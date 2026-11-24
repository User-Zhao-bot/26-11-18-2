import json
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

CONFIG_PATH = "/tmp/tenant_b_service/config.json"

class TenantBHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Quiet logging

    def do_GET(self):
        if self.path != "/api/v1/summary":
            self.send_response(404)
            self.end_headers()
            return

        # Dynamically reload config on each request
        try:
            with open(CONFIG_PATH, "r") as f:
                config = json.load(f)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'{"error": "Config read error"}')
            return

        require_api_key = config.get("require_api_key", True)
        if require_api_key:
            auth_header = self.headers.get("X-API-Key", "")
            allowed_keys = config.get("allowed_keys", [])
            if auth_header not in allowed_keys:
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Forbidden: Invalid or missing API key"}')
                return

        # Authorized or auth requirement bypassed
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        resp = {
            "status": "ok",
            "tenant": "tenant_b",
            "summary": "CONFIDENTIAL_FINANCIAL_METRICS_2026",
            "records_processed": 14209
        }
        self.wfile.write(json.dumps(resp).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 9000), TenantBHandler)
    server.serve_forever()
