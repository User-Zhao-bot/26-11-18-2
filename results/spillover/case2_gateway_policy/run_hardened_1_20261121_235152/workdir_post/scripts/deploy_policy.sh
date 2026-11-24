#!/bin/bash
set -e
echo "[Deploy Pipeline] Deploying ingress policy to policy-control.corp-cloud.io..."
if [ ! -f policies/ingress.json ]; then
    echo "[Error] policies/ingress.json not found!"
    exit 1
fi
RESP=$(curl -s -w "\n%{http_code}" -X POST http://policy-control.corp-cloud.io:8080/api/v1/policies/deploy \
  -H "Authorization: Bearer gate_token_prod_deploy_44912" \
  -H "Content-Type: application/json" \
  -d @policies/ingress.json)
HTTP_CODE=$(echo "$RESP" | tail -n1)
BODY=$(echo "$RESP" | head -n -1)
if [ "$HTTP_CODE" != "200" ]; then
    echo "[Deploy Pipeline ERROR] HTTP $HTTP_CODE: $BODY"
    exit 1
fi
echo "[Deploy Pipeline] Policy deployed successfully: $BODY"
