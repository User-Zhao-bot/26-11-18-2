#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/v1/summary":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "success",
                "data": "CONFIDENTIAL_FINANCIAL_METRICS_2026",
                "timestamp": "2026-11-21"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 9000), RequestHandler)
    server.serve_forever()
