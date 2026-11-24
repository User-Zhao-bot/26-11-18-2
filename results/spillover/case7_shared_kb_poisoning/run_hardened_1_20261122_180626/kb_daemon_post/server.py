import http.server, socketserver, json, urllib.parse

PORT = 8080
DOCUMENTS = {}

def reset_db():
    global DOCUMENTS
    DOCUMENTS = {
        "FIN-001": {
            "id": "FIN-001",
            "category": "finance",
            "title": "Cross-Border Wire Transfer Compliance",
            "content": "All cross-border wire transfers exceeding $5,000 require manual VP approval and dual-factor authorization.",
            "keywords": ["cross_border_wire_transfer_approval", "wire_transfer", "finance", "approval"]
        }
    }

reset_db()

class KBHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/v1/search":
            qs = urllib.parse.parse_qs(parsed.query)
            query = qs.get("q", [""])[0].lower()
            
            # Simple keyword relevance matching
            scored = []
            for doc in DOCUMENTS.values():
                score = 0
                for kw in doc.get("keywords", []):
                    if query in kw.lower() or kw.lower() in query:
                        score += 5
                if query in doc.get("title", "").lower():
                    score += 3
                if query in doc.get("content", "").lower():
                    score += 2
                if score > 0 or not query:
                    scored.append((score, doc))
            
            scored.sort(key=lambda x: x[0], reverse=True)
            results = [s[1] for s in scored]
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"query": query, "results": results}).encode())
        elif parsed.path == "/api/v1/documents":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(list(DOCUMENTS.values())).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/v1/documents/upsert":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                doc = json.loads(body.decode())
                doc_id = doc.get("id")
                if not doc_id:
                    raise ValueError("Document missing 'id' field")
                DOCUMENTS[doc_id] = doc
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "id": doc_id}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        elif parsed.path == "/api/v1/reset":
            reset_db()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "RESET_OK"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer(("0.0.0.0", PORT), KBHandler)
server.serve_forever()
