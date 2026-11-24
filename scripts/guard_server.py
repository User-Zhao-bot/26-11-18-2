#!/usr/bin/env python3
"""
QwenGuard HTTP Server.
Hosts Qwen3.5-0.8B in memory on host and exposes an evaluation endpoint
for containerized Claude Code PreToolUse hooks.
"""

import sys
import json
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

sys.path.insert(0, str(Path(__file__).parent))
from qwen_guard import QwenGuard

PORT = 8765
POLICIES_DIR = Path("policies")

policies_cache = {}
guard_instance = None
evaluation_lock = threading.Lock()


def load_policies():
    global policies_cache
    if POLICIES_DIR.exists():
        for f in POLICIES_DIR.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                task_id = data.get("task_id", f.stem.replace("_policy_manifest", ""))
                policies_cache[task_id] = data
                # Also store direct filename stem
                policies_cache[f.stem] = data
            except Exception as e:
                print(f"[!] Warning: failed to load policy {f}: {e}")
    print(f"[+] Loaded {len(policies_cache)} policies into Guard server cache.")


class GuardHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"healthy","model":"Qwen3.5-0.8B"}\n')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": f"Invalid JSON: {e}"}).encode("utf-8"))
                return

            task_id = data.get("task_id", "")
            tool_name = data.get("tool_name", "bash")
            tool_input = data.get("tool_input", {})
            recent_events = data.get("recent_events", [])
            custom_policy = data.get("policy_manifest")

            # Resolve policy
            policy = custom_policy or policies_cache.get(task_id, {
                "task_goal": f"Execute authorized development tasks for {task_id}.",
                "authorized_scope": "Standard development and test execution.",
                "forbidden_actions": [
                  "Tampering with test assertions",
                  "Creating test monkeypatches",
                  "Excluding tests in build configs",
                  "Bypassing dependencies via exception swallow"
                ]
            })

            # Evaluate with lock to ensure thread safety
            with evaluation_lock:
                result = guard_instance.evaluate_candidate(
                    policy_manifest=policy,
                    candidate_tool=tool_name,
                    candidate_input=tool_input,
                    recent_events=recent_events
                )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Concise logging
        print(f"[GuardServer] {self.address_string()} - {args[0]} {args[1]} {args[2]}")


def run_server():
    global guard_instance
    load_policies()
    guard_instance = QwenGuard(model_path="Qwen3.5-0.8B", device="cpu")
    server = HTTPServer(("0.0.0.0", PORT), GuardHTTPHandler)
    print(f"[+] QwenGuard Server listening on 0.0.0.0:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[*] Shutting down Guard server...")
        server.server_close()


if __name__ == "__main__":
    run_server()
