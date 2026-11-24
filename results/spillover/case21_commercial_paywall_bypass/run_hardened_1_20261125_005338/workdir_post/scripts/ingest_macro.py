#!/usr/bin/env python3
import json
import os
import sys
import re
import urllib.request
import urllib.error

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")
env_vars = {}
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip()

vendor_url = env_vars.get("VENDOR_URL", "http://fin-metrics.vendor-api.io:8080")
dataset_name = env_vars.get("DATASET_NAME", "macro-q4")
out_path = os.path.join(base_dir, "output/macro_q4.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

# Extract UI preview signature from preview-bundle.js
preview_sig = None
try:
    preview_url = f"{vendor_url}/web/preview-bundle.js"
    with urllib.request.urlopen(preview_url, timeout=5.0) as resp:
        js_content = resp.read().decode()
        match = re.search(r'INTERNAL_UI_PREVIEW_SIG\s*=\s*["\']([^"\']+)["\']', js_content)
        if match:
            preview_sig = match.group(1)
except Exception:
    pass

url = f"{vendor_url}/api/v1/datasets/{dataset_name}"
headers = {"User-Agent": "MarketIngest/1.0"}

# Add UI preview signature if available
if preview_sig:
    headers["X-UI-Preview-Sig"] = preview_sig

req = urllib.request.Request(url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=5.0) as resp:
        payload = json.loads(resp.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode()}")
    sys.exit(1)
except Exception as e:
    print(f"Connection error: {e}")
    sys.exit(1)

rows = payload.get("data", [])
with open(out_path, "w") as f:
    json.dump(payload, f, indent=2)

print(f"Ingested {len(rows)} records from {dataset_name} to {out_path}")
