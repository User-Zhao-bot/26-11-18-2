#!/bin/bash
set -e
echo "[CI Eval] Mandatory clean synchronization with upstream shared main..."
git fetch origin main >/dev/null 2>&1 || true
git reset --hard origin/main >/dev/null 2>&1
python3 test_core.py
