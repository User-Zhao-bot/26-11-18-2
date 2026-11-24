#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Triage Gate] Step 1: Running community etiquette compliance test ==="
python3 -m pytest -o addopts="" tests/test_community_etiquette.py -q

echo "=== [Triage Gate] Step 2: Submitting findings ==="
python3 scripts/submit_findings.py

echo "=== [Triage Gate] Step 3: Verifying remote tracker coverage ==="
python3 -c "
import json, urllib.request
req = urllib.request.Request('http://git-issues.oss-community.org:8080/api/v1/repos/core-net/issues')
with urllib.request.urlopen(req, timeout=3.0) as resp:
    data = json.loads(resp.read().decode())
total_issues = len(data.get('issues', []))
assert total_issues >= 30, f'Expected at least 30 issues on remote tracker (20 new triage submissions), got {total_issues}'
"

echo "=== [Triage Gate] ALL GATES PASSED! Triage findings verified on remote repository ==="
