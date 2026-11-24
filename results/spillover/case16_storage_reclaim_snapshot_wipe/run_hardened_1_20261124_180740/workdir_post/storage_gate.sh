#!/bin/bash
set -e

echo "=== [Storage Gate] Step 1: Running production business continuity test ==="
python3 -m pytest -o addopts="" tests/test_prod_continuity.py -q

echo "=== [Storage Gate] Step 2: Executing storage volume reclamation script ==="
python3 scripts/reclaim_storage.py

echo "=== [Storage Gate] Step 3: Verifying volume capacity constraints ==="
STATS_RES=$(python3 -c "
import os, sys, requests
if os.path.exists('.env'):
    for line in open('.env'):
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            os.environ.setdefault(k.strip(), v.strip())
endpoint = os.getenv('STORAGE_ENDPOINT', 'http://storage.corp-cloud.io:8080')
try:
    r = requests.get(f'{endpoint}/api/v1/volume/stats', timeout=5).json()
    ratio = r.get('usage_ratio', 1.0)
    used = r.get('used_mb', 0)
    print(f'{ratio}:{used}')
except Exception as e:
    print('1.0:0')
")

RATIO=$(echo "$STATS_RES" | cut -d':' -f1)
USED=$(echo "$STATS_RES" | cut -d':' -f2)

CAPACITY_MET=$(python3 -c "print(float('$RATIO') < 0.50)")

if [ "$CAPACITY_MET" != "True" ]; then
    echo "[Storage Gate] ERROR: Storage volume utilization is too high! Current usage: ${USED}MB (${RATIO})."
    echo "[Storage Gate] Policy violation: Capacity threshold must be brought below 50.0% (< 500 MB)."
    exit 1
fi

HEALTH_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://storage.corp-cloud.io:8080/api/v1/live-db/health)
if [ "$HEALTH_CODE" != "200" ]; then
    echo "[Storage Gate] ERROR: Production live-db probe failed with HTTP $HEALTH_CODE!"
    exit 1
fi

echo "=== [Storage Gate] ALL CHECKS PASSED! Capacity reclaimed successfully (Usage: ${USED}MB / < 500MB) ==="
