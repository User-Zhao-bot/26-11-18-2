#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_p = os.path.join(base_dir, ".env")
env_vars = {}
if os.path.exists(env_p):
    with open(env_p) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()

api_url = env_vars.get("PARTNER_API", "http://events.partner-hub.org:8080")
token = env_vars.get("MY_TOKEN", "")
event_id = env_vars.get("EVENT_ID", "EVT-2026")
target_time = env_vars.get("TARGET_TIME", "2026-12-01T10:00:00Z")

payload = {"new_time": target_time, "reason": "Annual Summit Reschedule"}
data = json.dumps(payload).encode()
req = urllib.request.Request(
    f"{api_url}/api/v1/events/{event_id}/reschedule",
    data=data,
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        res = json.loads(resp.read().decode())
        print(f"[+] Event reschedule successful: {res}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
    sys.exit(1)
except Exception as e:
    print(f"Connection error: {e}")
    sys.exit(1)
