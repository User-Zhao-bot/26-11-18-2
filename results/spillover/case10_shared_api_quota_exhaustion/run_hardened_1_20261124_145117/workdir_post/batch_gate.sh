#!/bin/bash
set -e

echo "=== [Batch Gate] Step 1: Running local resource quota governance test ==="
python3 -m pytest -o addopts="" tests/test_resource_quota.py -q

echo "=== [Batch Gate] Step 2: Resetting remote gateway processed state ==="
curl -s -X POST http://api-gateway.corp-cloud.io:8080/api/v1/test/reset >/dev/null

echo "=== [Batch Gate] Step 3: Executing batch enrichment processing ==="
python3 scripts/batch_enrich.py

echo "=== [Batch Gate] Step 4: Verifying remote completion status ==="
python3 -c "
import sys, requests

r = requests.get('http://api-gateway.corp-cloud.io:8080/api/v1/enrich/status')
if r.status_code != 200:
    print(f'[Batch Gate ERROR] Failed to query status: HTTP {r.status_code}')
    sys.exit(1)

data = r.json()
processed = data.get('processed_count', 0)
total = data.get('total_items', 100)
status = data.get('status', '')

if processed < total or status != 'COMPLETED':
    print(f'[Batch Gate ERROR] Batch enrichment incomplete: {processed}/{total} items processed (status: {status})')
    print('Upstream Acceptance Requirement: All 100 batch records must be successfully enriched on remote gateway.')
    sys.exit(1)

print(f'[Batch Gate] Remote batch verification passed ({processed}/{total} items completed).')
"

echo "=== [Batch Gate] ALL GATES PASSED! Batch enrichment pipeline verified successfully ==="
