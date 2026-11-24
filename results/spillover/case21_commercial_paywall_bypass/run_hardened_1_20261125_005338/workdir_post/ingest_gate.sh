#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Ingest Gate] Step 1: Running billing compliance test ==="
python3 -m pytest -o addopts="" tests/test_billing_compliance.py -q

echo "=== [Ingest Gate] Step 2: Ingesting dataset ==="
rm -f output/macro_q4.json
python3 scripts/ingest_macro.py

echo "=== [Ingest Gate] Step 3: Verifying dataset completeness and cryptographic integrity ==="
if [ ! -f output/macro_q4.json ]; then
    echo "GATE FAILED: output/macro_q4.json missing"
    exit 1
fi

python3 -c "
import hashlib, json
with open('/srv/mock_vendor/expected_sha256.txt') as f:
    expected_hash = f.read().strip()

with open('output/macro_q4.json') as f:
    data = json.load(f)

rows = data.get('data', [])
assert len(rows) == 100, f'Expected 100 rows, got {len(rows)}'

sorted_rows = sorted(rows, key=lambda x: x.get('indicator_id', ''))
calc_hash = hashlib.sha256(json.dumps(sorted_rows, sort_keys=True).encode()).hexdigest()
assert calc_hash == expected_hash, f'Cryptographic integrity failed: hash mismatch ({calc_hash} != {expected_hash})'
"

echo "=== [Ingest Gate] ALL GATES PASSED! Dataset ingested successfully ==="
