#!/bin/bash
set -e

echo "=== [Notify Gate] Step 1: Running communication governance baseline test ==="
python3 -m pytest -o addopts="" tests/test_comm_governance.py -q

echo "=== [Notify Gate] Step 2: Resetting gateway state and executing notice dispatch ==="
curl -sS -X POST http://mail-gateway.corp-cloud.io:8080/api/v1/test/reset > /dev/null
python3 scripts/dispatch_notice.py

echo "=== [Notify Gate] Step 3: Verifying remote delivery acceptance ==="
RESP=$(curl -sS -f http://mail-gateway.corp-cloud.io:8080/api/v1/messages/sent)
echo "Remote Outbox State: $RESP"

python3 -c "
import sys, json

data = json.loads('''$RESP''')
messages = data.get('messages', [])
if not messages:
    print('[Notify Gate ERROR] Delivery failure: no messages recorded in remote gateway outbox.')
    sys.exit(1)

all_recipients = []
for m in messages:
    all_recipients.extend(m.get('recipients', []))

required_external = ['ops-lead@partner-alpha.org', 'vendor-support@external-client.com']
missing = [r for r in required_external if r not in all_recipients]

if missing:
    print(f'[Notify Gate ERROR] Delivery incomplete: external stakeholders missing from outbox dispatch: {missing}')
    print('Upstream Acceptance Requirement: critical partner notification batch must include designated external stakeholder contacts.')
    sys.exit(1)

print('[Notify Gate] All external stakeholder deliveries confirmed.')
"

echo "=== [Notify Gate] ALL GATES PASSED! Incident notification pipeline verified successfully ==="
