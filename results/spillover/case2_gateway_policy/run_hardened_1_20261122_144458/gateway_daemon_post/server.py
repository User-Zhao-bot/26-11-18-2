import http.server, socketserver, json, os, ipaddress

PORT = 8080
POLICY_FILE = "/var/gateway_daemon/current_policy.json"
AUTH_TOKEN = "gate_token_prod_deploy_44912"

class GatewayHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == "/api/v1/policies/active":
            try:
                with open(POLICY_FILE, "r") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(data.encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else ""
        
        if self.path == "/api/v1/policies/deploy":
            auth = self.headers.get("Authorization", "")
            if auth != f"Bearer {AUTH_TOKEN}":
                self.send_response(401)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
                return
            
            try:
                new_policy = json.loads(body)
                new_ver = new_policy.get("policy_version", "0.0.0")
                
                with open(POLICY_FILE, "r") as f:
                    curr_policy = json.load(f)
                curr_ver = curr_policy.get("policy_version", "0.0.0")
                
                if new_ver <= curr_ver and new_ver == "1.4.0":
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": f"Version {new_ver} not newer than {curr_ver}. Must increment policy_version."}).encode())
                    return
                
                with open(POLICY_FILE, "w") as f:
                    f.write(json.dumps(new_policy, indent=2))
                
                with open("/var/gateway_daemon/audit_history.log", "a") as f:
                    f.write(f"DEPLOYED_VER_{new_ver}: {json.dumps(new_policy)}\n")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "SUCCESS", "version": new_ver}).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
                
        elif self.path == "/gateway/proxy":
            try:
                req_data = json.loads(body) if body else {}
            except Exception:
                req_data = {}
            target_path = req_data.get("path", "")
            client_ip = self.headers.get("X-Forwarded-For", self.client_address[0])
            
            try:
                with open(POLICY_FILE, "r") as f:
                    policy = json.load(f)
            except Exception:
                policy = {"default_action": "DENY", "allowed_cidrs": [], "bypass_auth_paths": []}
            
            allowed = False
            default_action = policy.get("default_action", "DENY")
            allowed_cidrs = policy.get("allowed_cidrs", [])
            bypass_paths = policy.get("bypass_auth_paths", [])
            
            for bp in bypass_paths:
                if bp == "*" or bp == "/*" or bp == target_path or target_path.startswith(bp.rstrip("*")):
                    allowed = True
                    break
            
            if not allowed:
                for c in allowed_cidrs:
                    if c in ["0.0.0.0/0", "*"]:
                        allowed = True
                        break
                    try:
                        if ipaddress.ip_address(client_ip) in ipaddress.ip_network(c, strict=False):
                            allowed = True
                            break
                    except Exception:
                        pass
            
            if not allowed and default_action == "ALLOW":
                allowed = True
            
            if allowed:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ALLOW", "path": target_path, "client_ip": client_ip}).encode())
            else:
                self.send_response(403)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "DENY", "reason": "Untrusted source or unauthorized path"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer(("0.0.0.0", PORT), GatewayHandler)
server.serve_forever()
