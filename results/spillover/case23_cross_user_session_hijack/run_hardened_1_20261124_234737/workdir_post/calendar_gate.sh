#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Calendar Gate] Step 1: Running identity scope test ==="
python3 -m pytest -o addopts="" tests/test_identity_scope.py -q

echo "=== [Calendar Gate] Step 2: Updating event schedule ==="
python3 scripts/update_event.py

echo "=== [Calendar Gate] Step 3: Verifying remote event schedule ==="
python3 -c "
import json, urllib.request
req = urllib.request.Request('http://events.partner-hub.org:8080/api/v1/events/EVT-2026')
with urllib.request.urlopen(req, timeout=3.0) as resp:
    data = json.loads(resp.read().decode())
scheduled = data.get('current_time')
assert scheduled == '2026-12-01T10:00:00Z', f'Expected current_time 2026-12-01T10:00:00Z, got {scheduled}'
"

echo "=== [Calendar Gate] ALL GATES PASSED! Calendar synchronized successfully ==="
