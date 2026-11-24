import http.server, socketserver, json, psycopg2

PORT = 8080
DB_URL = "postgresql://svc_migrator:migrator_pass_991@127.0.0.1:5432/prod_ledger"

class BillingAPIHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/api/v1/ledger/active-totals":
            try:
                conn = psycopg2.connect(DB_URL)
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) AS total_active_rows, COALESCE(SUM(amount), 0) AS total_active_amount FROM account_ledger WHERE status = 'ACTIVE';")
                row = cur.fetchone()
                total_rows = row[0]
                total_amount = float(row[1])
                conn.close()

                resp_data = {
                    "total_active_rows": total_rows,
                    "total_active_amount": total_amount
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resp_data).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer(("0.0.0.0", PORT), BillingAPIHandler)
server.serve_forever()
