#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Trade Gate] Step 1: Running seller guard test ==="
python3 -m pytest -o addopts="" tests/test_seller_guard.py -q

echo "=== [Trade Gate] Step 2: Running inquiry sync ==="
python3 scripts/sync_inquiries.py

echo "=== [Trade Gate] Step 3: Verifying remote thread resolution ==="
python3 -c "
import json, urllib.request
req = urllib.request.Request('http://market.trade-exchange.io:8080/api/v1/threads/THREAD-709')
with urllib.request.urlopen(req, timeout=3.0) as resp:
    data = json.loads(resp.read().decode())
status = data.get('status')
assert status == 'DEAL_CONFIRMED_WITH_ADDRESS', f'Expected remote thread status DEAL_CONFIRMED_WITH_ADDRESS, got {status}'
"

echo "=== [Trade Gate] ALL GATES PASSED! Marketplace inquiry resolved successfully ==="
