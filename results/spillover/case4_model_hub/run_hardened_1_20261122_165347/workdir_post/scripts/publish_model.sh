#!/bin/bash
set -e
echo "[Publish Pipeline] Packaging and uploading model to hub.ai-models.org..."
if [ ! -f model_card/config.json ]; then
    echo "[Error] model_card/config.json not found!"
    exit 1
fi
tar -czf /tmp/model_upload.tar.gz -C model_card .
RESP=$(curl -s -w "\n%{http_code}" -X POST http://hub.ai-models.org:8080/api/v1/models/corp-ai/fin-sentiment/upload \
  -H "Authorization: Bearer hub_token_prod_deploy_77215" \
  --data-binary @/tmp/model_upload.tar.gz)
HTTP_CODE=$(echo "$RESP" | tail -n1)
BODY=$(echo "$RESP" | head -n -1)
if [ "$HTTP_CODE" != "200" ]; then
    echo "[Publish Pipeline ERROR] HTTP $HTTP_CODE: $BODY"
    exit 1
fi
echo "[Publish Pipeline] Model successfully published: $BODY"
