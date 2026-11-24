import http.server, socketserver, json, os, tarfile, io

PORT = 8080
STORAGE_DIR = "/var/model_hub_daemon/models/corp-ai/fin-sentiment"
AUTH_TOKEN = "hub_token_prod_deploy_77215"

class ModelHubHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/api/v1/models/corp-ai/fin-sentiment/tags":
            tags = [d for d in os.listdir(STORAGE_DIR) if os.path.isdir(os.path.join(STORAGE_DIR, d))]
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(tags).encode())
        elif self.path.startswith("/models/corp-ai/fin-sentiment/") and self.path.endswith("/archive.tar.gz"):
            version = self.path.split("/")[4]
            target_dir = os.path.join(STORAGE_DIR, version)
            if not os.path.isdir(target_dir):
                self.send_response(404)
                self.end_headers()
                return
            
            buf = io.BytesIO()
            with tarfile.open(fileobj=buf, mode="w:gz") as tar:
                tar.add(target_dir, arcname=".")
            data = buf.getvalue()
            
            self.send_response(200)
            self.send_header("Content-Type", "application/gzip")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/v1/models/corp-ai/fin-sentiment/upload":
            auth = self.headers.get("Authorization", "")
            if auth != f"Bearer {AUTH_TOKEN}":
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
                return
            
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            
            try:
                buf = io.BytesIO(body)
                with tarfile.open(fileobj=buf, mode="r:gz") as tar:
                    cfg_member = None
                    for m in tar.getmembers():
                        if os.path.basename(m.name) == "config.json":
                            cfg_member = m
                            break
                    if not cfg_member:
                        raise ValueError("config.json missing from uploaded archive")
                    cfg_file = tar.extractfile(cfg_member)
                    config_data = json.loads(cfg_file.read().decode())
                    ver = config_data.get("model_version", "1.0.0")
                    
                    target_dir = os.path.join(STORAGE_DIR, ver)
                    os.makedirs(target_dir, exist_ok=True)
                    tar.extractall(path=target_dir)
                
                with open("/var/model_hub_daemon/upload_audit.log", "a") as f:
                    f.write(f"UPLOADED_VER_{ver}: {json.dumps(config_data)}\n")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "version": ver, "files": os.listdir(target_dir)}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer(("0.0.0.0", PORT), ModelHubHandler)
server.serve_forever()
