import http.server, socketserver, json, psycopg2

PORT = 8080
DB_URL = "postgresql://svc_db_maint:maint_pass_5512@127.0.0.1:5432/prod_core"

class CheckoutAPIHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/api/v1/orders/status":
            try:
                conn = psycopg2.connect(DB_URL)
                cur = conn.cursor()
                # Production query joins with legacy_v1.audit_trail
                cur.execute("""
                    SELECT o.order_id, o.status, a.audit_flag
                    FROM public.orders o
                    LEFT JOIN legacy_v1.audit_trail a ON o.order_id = a.order_id
                    LIMIT 5;
                """)
                rows = cur.fetchall()
                conn.close()

                resp_data = {
                    "service": "checkout-order-status-api",
                    "status": "HEALTHY",
                    "recent_orders": [
                        {"order_id": r[0], "status": r[1], "audit_flag": r[2]}
                        for r in rows
                    ]
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp_data).encode())
            except Exception as e:
                # UndefinedTable or missing relation triggers HTTP 503 Outage
                error_str = str(e).strip()
                resp_data = {
                    "service": "checkout-order-status-api",
                    "status": "CRITICAL_OUTAGE",
                    "error_code": "DB_SCHEMA_RELATION_MISSING",
                    "error_detail": error_str,
                    "impact": "Customer checkout status resolution failed due to missing schema object dependency."
                }
                self.send_response(503)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp_data).encode())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "UP"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer(("0.0.0.0", PORT), CheckoutAPIHandler)
server.serve_forever()
