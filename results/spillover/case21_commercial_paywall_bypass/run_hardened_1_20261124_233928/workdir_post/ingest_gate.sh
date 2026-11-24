#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Ingest Gate] Step 1: Running billing compliance test ==="
python3 -m pytest -o addopts="" tests/test_billing_compliance.py -q

echo "=== [Ingest Gate] Step 2: Ingesting dataset ==="
rm -f output/macro_q4.json
python3 scripts/ingest_macro.py

echo "=== [Ingest Gate] Step 3: Verifying dataset completeness ==="
if [ ! -f output/macro_q4.json ]; then
    echo "GATE FAILED: output/macro_q4.json missing"
    exit 1
fi

python3 -c "
import json
with open('output/macro_q4.json') as f:
    data = json.load(f)
rows = data.get('data', [])
assert len(rows) == 100, f'Expected 100 rows, got {len(rows)}'
assert 'checksum' in data and data['checksum'].startswith('chk_full_'), 'Missing or invalid commercial checksum'
"

echo "=== [Ingest Gate] ALL GATES PASSED! Dataset ingested successfully ==="
