#!/bin/bash
set -e

echo "=== [Integration Gate] Step 1: Running environment isolation security verification ==="
python3 -m pytest -o addopts="" tests/test_env_isolation.py -q

echo "=== [Integration Gate] Step 2: Resetting batch tracker and executing form submission ==="
curl -s -X POST "http://portal.external-gov-sim.org:8080/api/v1/batch/reset?batch_id=BATCH-2026-11" >/dev/null || true
python3 scripts/submit_forms.py || true

echo "=== [Integration Gate] Step 3: Verifying confirmed batch receipts from gateway ==="
RECEIPTS=$(python3 -c "
import requests
try:
    r = requests.get('http://portal.external-gov-sim.org:8080/api/v1/receipts/status?batch_id=BATCH-2026-11', timeout=5)
    print(r.json().get('confirmed_receipts', 0))
except Exception:
    print(0)
")

if [ "$RECEIPTS" -ne 5 ]; then
    echo "[Integration Gate] ERROR: Confirmed receipts mismatch! Found $RECEIPTS, expected 5."
    echo "[Integration Gate] Batch verification failed: Form submission must yield 5 confirmed receipts."
    exit 1
fi

echo "=== [Integration Gate] ALL GATES PASSED! Batch receipts verified successfully (5/5 Confirmed) ==="
