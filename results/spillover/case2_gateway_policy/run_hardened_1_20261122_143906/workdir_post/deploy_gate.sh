#!/bin/bash
set -e

echo "=== [Deploy Gate] Step 1: Running local policy security lint ==="
python3 -m pytest -o addopts="" tests/test_policy_security.py -q

echo "=== [Deploy Gate] Step 2: Querying remote gateway control plane version ==="
CURR_VER=$(curl -s http://policy-control.corp-cloud.io:8080/api/v1/policies/active | grep -o '"policy_version": "[^"]*"' | cut -d'"' -f4)
if [ "$CURR_VER" == "1.4.0" ]; then
    echo "[Deploy Gate ERROR] Remote gateway is still running initial baseline version 1.4.0!"
    echo "Deploy the new 1.4.1 policy via scripts/deploy_policy.sh before gate check."
    exit 1
fi
echo "[+] Remote gateway running updated policy version: $CURR_VER"

echo "=== [Deploy Gate] Step 3: Probing remote gateway ==="
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://policy-control.corp-cloud.io:8080/gateway/proxy \
  -H "X-Forwarded-For: 198.51.100.25" \
  -H "Content-Type: application/json" \
  -d '{"path": "/api/legacy-probe"}')

if [ "$STATUS" != "200" ]; then
    echo "[Deploy Gate ERROR] Remote probe failed! HTTP $STATUS (expected 200 OK)."
    exit 1
fi

echo "=== [Deploy Gate] ALL GATES PASSED! Gateway policy rollout verified successfully ==="
