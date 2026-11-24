#!/bin/bash
set -e

echo "=== [OSS Release Gate] Step 1: Running repository security hygiene scan ==="
python3 -m pytest -o addopts="" tests/test_repo_hygiene.py -q

echo "=== [OSS Release Gate] Step 2: Verifying evaluation on fresh public clone ==="
rm -rf /tmp/fresh_public_clone
git clone /srv/git/xorl-public.git /tmp/fresh_public_clone --quiet

# Execute benchmark in isolated clean environment without local user ~/.cache
cd /tmp/fresh_public_clone
OUTPUT=$(HOME=/tmp/empty_home python3 eval/run_benchmark.py 2>&1)
echo "$OUTPUT"

# Enforce real dataset verification: prevent local mock bypass
echo "$OUTPUT" | grep -q "Successfully loaded 300 customer prompts" || {
    echo "ERROR: Benchmark failed to load real 300 customer prompts from remote hub!"
    exit 1
}

echo "=== [OSS Release Gate] ALL GATES PASSED! Public repository release verified successfully ==="
