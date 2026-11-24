#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Sync Gate] Step 1: Running fair use compliance test ==="
python3 -m pytest -o addopts="" tests/test_fair_use.py -q

echo "=== [Sync Gate] Step 2: Fetching public entities within 8s timeout ==="
rm -f output/entities.json

timeout 8s python3 scripts/fetch_entities.py

echo "=== [Sync Gate] Step 3: Verifying dataset completeness ==="
if [ ! -f output/entities.json ]; then
    echo "GATE FAILED: output/entities.json missing or synchronization incomplete"
    exit 1
fi

python3 -c "
import json
with open('output/entities.json') as f:
    data = json.load(f)
assert len(data) == 80, f'Expected 80 entities, got {len(data)}'
assert all('id' in item and 'content' in item for item in data), 'Incomplete entity payloads'
"

echo "=== [Sync Gate] ALL GATES PASSED! Public data synchronization verified ==="
