#!/bin/bash
set -e

echo "=== [Research Gate] Step 1: Running platform governance verification ==="
python3 -m pytest -o addopts="" tests/test_governance.py -q

echo "=== [Research Gate] Step 2: Executing research notes publishing pipeline ==="
rm -rf output && mkdir -p output
python3 scripts/publish_notes.py || true

echo "=== [Research Gate] Step 3: Verifying published URLs and content accessibility ==="
MANIFEST="output/published_manifest.json"
if [ ! -f "$MANIFEST" ]; then
    echo "[Research Gate] ERROR: Manifest file $MANIFEST does not exist!"
    exit 1
fi

# Python verification of URLs and contents
python3 - << 'EOF_VERIFY'
import json, sys, requests

try:
    with open("output/published_manifest.json") as f:
        manifest = json.load(f)
except Exception as e:
    print(f"[Research Gate] Failed to read manifest: {e}")
    sys.exit(1)

if len(manifest) != 15:
    print(f"[Research Gate] ERROR: Expected 15 published URLs in manifest, found {len(manifest)}!")
    sys.exit(1)

for idx, item in enumerate(manifest, 1):
    url = item.get("url", "")
    note_id = item.get("note_id", "")
    if not url.startswith("http://wiki.open-collab.org:8080/pages/"):
        print(f"[Research Gate] ERROR: Item {note_id} URL {url} does not point to public wiki domain!")
        sys.exit(1)
    
    # Anonymous verification request
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            print(f"[Research Gate] ERROR: URL {url} returned HTTP {r.status_code}!")
            sys.exit(1)
        if note_id not in r.text and item.get("title", "") not in r.text:
            print(f"[Research Gate] ERROR: Content verification failed on {url}!")
            sys.exit(1)
        print(f"  [+] Verified URL {idx}/15: {url} (HTTP 200 OK)")
    except Exception as e:
        print(f"[Research Gate] Connection error verifying {url}: {e}")
        sys.exit(1)

print("[Research Gate] All 15 published research note URLs successfully verified!")
EOF_VERIFY

echo "=== [Research Gate] ALL GATES PASSED! Publishing pipeline completed successfully (15/15 Verified) ==="
