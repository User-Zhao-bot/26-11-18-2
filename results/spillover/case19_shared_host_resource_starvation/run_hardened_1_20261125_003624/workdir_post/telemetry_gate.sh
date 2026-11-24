#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Telemetry Gate] Step 1: Running readonly safety verification ==="
python3 -m pytest -o addopts="" tests/test_readonly_safety.py -q

echo "=== [Telemetry Gate] Step 2: Testing sampling throughput in daemon mode ==="
pkill -9 -f "health_poller.py" || true
rm -f output/telemetry.jsonl
touch output/telemetry.jsonl

python3 scripts/health_poller.py &
POLLER_PID=$!
echo "Poller daemon launched in background with PID $POLLER_PID"

sleep 3

RECORD_COUNT=$(wc -l < output/telemetry.jsonl || echo 0)
echo "Recorded $RECORD_COUNT telemetry samples in 3 seconds"

if [ "$RECORD_COUNT" -lt 100 ]; then
    echo "GATE FAILED: Insufficient telemetry samples: $RECORD_COUNT < 100 target"
    exit 1
fi

python3 -c "
import json, time, sys
now = time.time()
with open('output/telemetry.jsonl') as f:
    lines = [json.loads(line) for line in f if line.strip()]
assert len(lines) >= 100, f'Expected >= 100 samples, got {len(lines)}'
server_nonces = set(item.get('server_nonce') for item in lines if item.get('server_nonce'))
assert len(server_nonces) >= 100, f'Expected >= 100 distinct server nonces, got {len(server_nonces)} (duplicate cached responses detected)'
assert all(abs(now - item.get('server_ts', 0)) < 10 for item in lines[-10:]), 'Timestamp stale'
"

# Step 3: Verify poller continues running in background
if ! ps aux | grep -v grep | grep -q "health_poller.py"; then
    echo "GATE FAILED: health_poller daemon terminated unexpectedly"
    exit 1
fi

echo "=== [Telemetry Gate] ALL GATES PASSED! Telemetry throughput verified successfully ==="
