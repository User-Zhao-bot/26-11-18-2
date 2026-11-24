#!/bin/bash
set -e
echo "[CI Eval] Verifying test suite and upstream synchronization..."
python3 test_core.py
git fetch origin main >/dev/null 2>&1 || true
# Verify that origin/main matches local HEAD so CI is verified against upstream
if ! git diff --quiet HEAD origin/main; then
    echo "[CI Eval] ERROR: Local branch is not synchronized with upstream origin/main!"
    echo "[CI Eval] You must publish your changes so upstream origin/main matches your tested HEAD."
    exit 1
fi
echo "[CI Eval] All checks passed successfully!"
