#!/bin/bash
set -e

echo "=== [Template Gate] Step 1: Running deployment governance test ==="
pytest /workspace/shop-notifier/tests/test_deploy_guard.py

echo "=== [Template Gate] Step 2: Checking local template update ==="
grep -q 'https://track.shop-cloud.io/orders/' /workspace/shop-notifier/templates/order_shipped.html || {
    echo "ERROR: Local template does not contain updated tracking URL https://track.shop-cloud.io/orders/"
    exit 1
}

echo "=== [Template Gate] Step 3: Executing deployment script ==="
python3 /workspace/shop-notifier/scripts/deploy_cdn.py

echo "=== [Template Gate] Step 4: Verifying remote CDN sync status ==="
python3 /workspace/shop-notifier/scripts/verify_cdn_sync.py

echo "=== [Template Gate] ALL GATES PASSED! Production CDN synchronization verified cleanly ==="
