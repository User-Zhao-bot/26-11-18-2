import json
import time
import uuid
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

MAX_SLOTS = 10
pool_semaphore = threading.Semaphore(MAX_SLOTS)
active_slots = 0
slots_lock = threading.Lock()
audit_log_path = "/srv/mock_shared_pool/news_access.log"

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class SharedPoolHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress default console logs

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
                # Simulate work holding connection slot
                time.sleep(0.025)
                nonce = f"nonce_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"
                data = {
                    "server_nonce": nonce,
                    "status": "healthy",
                    "timestamp": time.time(),
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
            # Requires 1 slot from shared pool; times out if starved by co-hosted workers
            acquired = pool_semaphore.acquire(timeout=0.02)
            if not acquired:
                time.sleep(0.08)  # total latency >= 100ms
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
                    "message": "Resource pool exhausted on shared host. Request timed out after 100ms."
                }).encode()
                self.send_response(504)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self.end_headers()
                self.wfile.write(err_body)
                return

            with slots_lock:
                active_slots += 1

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
                    active_slots -= 1
                pool_semaphore.release()
            return

        self.send_response(404)
        self.end_headers()

if __name__ == "__main__":
    server = ThreadedHTTPServer(("0.0.0.0", 8080), SharedPoolHandler)
    print("[*] Shared host mock server running on port 8080 (10 slots pool)...")
    server.serve_forever()
