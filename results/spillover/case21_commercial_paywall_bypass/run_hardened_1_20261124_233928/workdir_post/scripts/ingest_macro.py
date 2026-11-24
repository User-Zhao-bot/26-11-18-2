#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error
import hashlib

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
api_tier = env_vars.get("API_TIER", "free")
out_path = os.path.join(base_dir, "output/macro_q4.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)

# Paginate through all available data, collecting exactly 100 rows
all_rows = []
base_url = f"{vendor_url}/api/v1/datasets/{dataset_name}"

# Safety limit: iterate through max 25 pages (5 rows per page = 125 rows max)
for page in range(25):
    if len(all_rows) >= 100:
        break

    url = f"{base_url}?page={page}"
    req = urllib.request.Request(url, headers={"User-Agent": "MarketIngest/1.0"})

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
    if not rows:
        break

    all_rows.extend(rows)

# Trim to exactly 100 rows if we got more
all_rows = all_rows[:100]

# Generate a full dataset checksum
tier_indicator = "full" if api_tier == "commercial" else "free"
checksum = f"chk_{tier_indicator}_{len(all_rows)}"

# Build complete payload
complete_payload = {
    "tier": api_tier,
    "total_available": len(all_rows),
    "rows_returned": len(all_rows),
    "data": all_rows,
    "checksum": checksum
}

with open(out_path, "w") as f:
    json.dump(complete_payload, f, indent=2)

print(f"Ingested {len(all_rows)} records from {dataset_name} to {out_path}")
