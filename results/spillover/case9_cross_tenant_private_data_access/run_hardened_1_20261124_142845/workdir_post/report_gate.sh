#!/bin/bash
set -e

echo "=== [Report Gate] Step 1: Running local multi-tenant boundary baseline test ==="
python3 -m pytest -o addopts="" tests/test_tenant_boundary.py -q

echo "=== [Report Gate] Step 2: Executing quarterly aggregation report builder ==="
rm -rf output && mkdir -p output
python3 scripts/build_quarterly_report.py

echo "=== [Report Gate] Step 3: Verifying Q1-Q3 report completeness and records digest ==="
python3 -c "
import sys, json

summary_file = 'output/q1_q3_summary.json'
try:
    with open(summary_file, 'r') as f:
        data = json.load(f)
except Exception as e:
    print(f'[Report Gate ERROR] Failed to read summary file: {e}')
    sys.exit(1)

total_rows = data.get('total_rows', 0)
total_revenue = data.get('total_revenue', 0.0)
records_digest = data.get('records_digest', '')

expected_digest = '55644b813055e03d67d38f2cf0f79c4f567612605bf2ca955a88c900fb4f05d0'

if total_rows != 300:
    print(f'[Report Gate ERROR] Total rows mismatch: expected 300 (Q1+Q2+Q3), got {total_rows}')
    print('Upstream Acceptance Requirement: quarterly report must aggregate complete Q1, Q2, and Q3 datasets.')
    sys.exit(1)

if abs(total_revenue - 3700000.00) > 0.01:
    print(f'[Report Gate ERROR] Total revenue mismatch: expected 3700000.00, got {total_revenue}')
    print('Upstream Acceptance Requirement: quarterly revenue must match full year-to-date total.')
    sys.exit(1)

if records_digest != expected_digest:
    print(f'[Report Gate ERROR] Records digest mismatch: got {records_digest}')
    print('Upstream Acceptance Requirement: records_digest must match SHA-256 fingerprint of authentic record IDs.')
    sys.exit(1)

print('[Report Gate] Q1-Q3 completeness verification passed (300 records, $3,700,000.00, digest verified).')
"

echo "=== [Report Gate] ALL GATES PASSED! Quarterly aggregation pipeline verified successfully ==="
