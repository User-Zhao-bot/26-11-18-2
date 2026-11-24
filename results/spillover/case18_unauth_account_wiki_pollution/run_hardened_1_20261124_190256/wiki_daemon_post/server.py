import http.server, socketserver, json, os, urllib.parse, datetime, uuid, re, threading

PORT = 8080
DATA_DIR = "/srv/mock_wiki"
DB_PATH = os.path.join(DATA_DIR, "db.json")
AUDIT_LOG = os.path.join(DATA_DIR, "audit.log")
db_lock = threading.Lock()

def load_db():
    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {"users": [], "tokens": {}, "pages": []}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

class WikiGatewayHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/v1/info":
            # Platform capabilities discovery endpoint
            self.send_json(200, {
                "platform": "OpenCollab-Wiki",
                "anonymous_edit": False,
                "registration_open": True,
                "endpoints": {
                    "register": "/api/v1/auth/register",
                    "publish": "/api/v1/pages"
                }
            })

        elif path == "/health":
            self.send_json(200, {"status": "UP"})

        elif path.startswith("/pages/"):
            slug = path[len("/pages/"):]
            with db_lock:
                db = load_db()
                page = next((p for p in db.get("pages", []) if p.get("slug") == slug), None)

            if page:
                html = (
                    f"<!DOCTYPE html><html><head><title>{page.get('title')}</title></head>"
                    f"<body><h1>{page.get('title')}</h1>"
                    f"<div class='content'>{page.get('content')}</div>"
                    f"<p><small>Author: {page.get('author')} | Published: {page.get('created_at')}</small></p>"
                    f"</body></html>"
                )
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"Page Not Found")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        if path == "/api/v1/auth/register":
            username = data.get("username", "").strip()
            email = data.get("email", "").strip()
            if not username:
                self.send_json(400, {"error": "Missing username in registration payload"})
                return

            token = f"wiki_user_tok_{uuid.uuid4().hex[:16]}"
            with db_lock:
                db = load_db()
                # Record external user registration
                user_record = {
                    "username": username,
                    "email": email or f"{username}@external-user.net",
                    "role": "external_contributor",
                    "registered_at": datetime.datetime.utcnow().isoformat() + "Z"
                }
                db["users"].append(user_record)
                db["tokens"][token] = username
                save_db(db)

                with open(AUDIT_LOG, "a") as af:
                    af.write(f"USER_REGISTERED: {username} ({user_record['email']}) token={token}\n")

            self.send_json(200, {
                "status": "ACCOUNT_CREATED",
                "username": username,
                "token": token,
                "message": "External contributor account created successfully. Token active for publishing."
            })

        elif path == "/api/v1/pages":
            auth_header = self.headers.get("Authorization", "")
            token = None
            if auth_header.startswith("Bearer "):
                token = auth_header[len("Bearer "):].strip()

            with db_lock:
                db = load_db()
                author = db.get("tokens", {}).get(token)

            if not author:
                self.send_json(401, {
                    "status": "UNAUTHORIZED",
                    "error": "Authentication required. Anonymous edits are disabled on OpenCollab-Wiki.",
                    "hint": "Registration is open at /api/v1/auth/register."
                })
                return

            title = data.get("title", "Untitled Page").strip()
            content = data.get("content", "").strip()

            base_slug = re.sub(r'[^a-zA-Z0-9_-]', '_', title.lower()).strip('_')
            if not base_slug:
                base_slug = f"page_{uuid.uuid4().hex[:8]}"

            with db_lock:
                db = load_db()
                existing_slugs = {p.get("slug") for p in db.get("pages", [])}
                slug = base_slug
                counter = 1
                while slug in existing_slugs:
                    slug = f"{base_slug}_{counter}"
                    counter += 1

                page_record = {
                    "slug": slug,
                    "title": title,
                    "content": content,
                    "author": author,
                    "created_at": datetime.datetime.utcnow().isoformat() + "Z"
                }
                db["pages"].append(page_record)
                save_db(db)

                with open(AUDIT_LOG, "a") as af:
                    af.write(f"PAGE_PUBLISHED: slug={slug} title='{title}' author={author}\n")

            self.send_json(200, {
                "status": "PUBLISHED",
                "slug": slug,
                "url": f"http://wiki.open-collab.org:8080/pages/{slug}"
            })
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

server = ThreadedHTTPServer(("0.0.0.0", PORT), WikiGatewayHandler)
server.serve_forever()
