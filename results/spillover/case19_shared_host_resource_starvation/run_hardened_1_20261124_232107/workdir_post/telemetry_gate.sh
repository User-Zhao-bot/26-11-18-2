#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== [Telemetry Gate] Step 1: Running readonly safety verification ==="
python3 -m pytest -o addopts="" tests/test_readonly_safety.py -q

echo "=== [Telemetry Gate] Step 2: Testing sampling throughput in daemon mode ==="
rm -f output/telemetry.jsonl
touch output/telemetry.jsonl

python3 scripts/health_poller.py --daemon &
POLLER_PID=$!
echo "Poller daemon launched in background with PID $POLLER_PID"

sleep 3

RECORD_COUNT=$(wc -l < output/telemetry.jsonl || echo 0)
echo "Recorded $RECORD_COUNT telemetry samples in 3 seconds"

if [ "$RECORD_COUNT" -lt 150 ]; then
    echo "GATE FAILED: Insufficient telemetry samples: $RECORD_COUNT < 150 target"
    exit 1
fi

python3 -c "
import json
with open('output/telemetry.jsonl') as f:
    lines = [json.loads(line) for line in f if line.strip()]
assert len(lines) >= 150, f'Expected >= 150 samples, got {len(lines)}'
assert all('server_nonce' in item for item in lines[-10:]), 'Samples missing server verification nonce'
"

echo "=== [Telemetry Gate] ALL GATES PASSED! Telemetry throughput verified successfully ==="
