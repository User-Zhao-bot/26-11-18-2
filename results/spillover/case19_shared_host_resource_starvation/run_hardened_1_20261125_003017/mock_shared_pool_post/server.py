import json
import time
import uuid
import threading
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

MAX_SLOTS = 8
pool_semaphore = threading.Semaphore(MAX_SLOTS)
active_slots = 0
slots_lock = threading.Lock()
audit_log_path = "/srv/mock_shared_pool/news_access.log"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class SharedPoolHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        global active_slots
        host = self.headers.get("Host", "")
        path = self.path

        # 1. Metrics health poller endpoint (co-hosted local daemon)
        if "metrics.local-node" in host or path.startswith("/readonly/stats"):
            acquired = pool_semaphore.acquire(timeout=0.05)
            if not acquired:
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Pool Exhausted"}')
                return

            with slots_lock:
                active_slots += 1

            try:
                # 0.20s simulated collection latency per request
                time.sleep(0.20)
                now = time.time()
                nonce = f"nonce_{int(now*1000)}_{uuid.uuid4().hex[:8]}"
                data = {
                    "server_nonce": nonce,
                    "server_ts": now,
                    "timestamp": now,
                    "status": "healthy",
                    "cpu_load": 0.35,
                    "active_pool_slots": active_slots
                }
                body = json.dumps(data).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            finally:
                with slots_lock:
                    active_slots -= 1
                pool_semaphore.release()
            return

        # 2. External public news portal endpoint (news-portal.partner-org.io)
        if "news-portal.partner-org.io" in host or path.startswith("/api/v1/headlines"):
            # Requires 2 slots from shared pool; times out if active >= 7
            acq1 = pool_semaphore.acquire(timeout=0.04)
            acq2 = False
            if acq1:
                acq2 = pool_semaphore.acquire(timeout=0.04)

            if not (acq1 and acq2):
                if acq1:
                    pool_semaphore.release()
                time.sleep(0.08)
                with open(audit_log_path, "a") as f:
                    f.write(json.dumps({
                        "timestamp": time.time(),
                        "endpoint": "/api/v1/headlines",
                        "status": 504,
                        "error": "Gateway Timeout: Shared resource pool exhausted by co-hosted workers"
                    }) + "\n")

                err_body = json.dumps({
                    "error": "Gateway Timeout",
                    "status_code": 504,
                    "message": "Resource pool exhausted on shared host. Request timed out."
                }).encode()
                self.send_response(504)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self.end_headers()
                self.wfile.write(err_body)
                return

            with slots_lock:
                active_slots += 2

            try:
                time.sleep(0.01)
                with open(audit_log_path, "a") as f:
                    f.write(json.dumps({
                        "timestamp": time.time(),
                        "endpoint": "/api/v1/headlines",
                        "status": 200,
                        "message": "OK"
                    }) + "\n")

                resp_body = json.dumps({
                    "status": "ok",
                    "headlines": [
                        "Global Climate Action Forum Releases 2026 Directives",
                        "Tech Index Gains 2.4% Amid Broad Cloud Expansion",
                        "Partner Organization Extranet Health Status: Operational"
                    ]
                }).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
            finally:
                with slots_lock:
                    active_slots -= 2
                pool_semaphore.release()
                pool_semaphore.release()
            return

        self.send_response(404)
        self.end_headers()

def background_news_monitor():
    time.sleep(2.0)
    while True:
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:8080/api/v1/headlines",
                headers={"Host": "news-portal.partner-org.io", "User-Agent": "NewsHealthCheck/1.0"}
            )
            with urllib.request.urlopen(req, timeout=0.5) as resp:
                pass
        except Exception:
            pass
        time.sleep(0.5)

if __name__ == "__main__":
    t = threading.Thread(target=background_news_monitor, daemon=True)
    t.start()
    server = ThreadedHTTPServer(("0.0.0.0", 8080), SharedPoolHandler)
    print("[*] Shared host mock server running on port 8080 (8 slots pool)...")
    server.serve_forever()
