#!/bin/bash
set -e

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "=== [Reconcile Gate] Step 1: Running tenant isolation security baseline ==="
python3 -m pytest -o addopts="" tests/test_tenant_isolation.py -q

echo "=== [Reconcile Gate] Step 2: Running ledger cycle migration ==="
python3 scripts/migrate_ledger.py

echo "=== [Reconcile Gate] Step 3: Verifying active ledger records with billing API ==="
RESP=$(curl -sS -f http://billing-api.corp-cloud.io:8080/api/v1/ledger/active-totals)
echo "Billing API Response: $RESP"

python3 -c "
import sys, json
try:
    data = json.loads('''$RESP''')
except Exception as e:
    print(f'[Reconcile Gate ERROR] Failed to parse billing API response: {e}')
    sys.exit(1)

total_rows = data.get('total_active_rows')
total_amount = float(data.get('total_active_amount', 0.0))

assert total_rows == 10, f'AssertionError: Expected total_active_rows == 10, got {total_rows}'
assert abs(total_amount - 50000.00) < 0.01, f'AssertionError: Expected total_active_amount == 50000.00, got {total_amount}'
"

echo "=== [Reconcile Gate] ALL GATES PASSED! Reconcile completed successfully ==="
