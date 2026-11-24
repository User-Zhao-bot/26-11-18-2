#!/bin/bash
set -e
echo "[CI Eval] Re-creating isolated temporary virtual environment..."
rm -rf /tmp/venv_eval
python3 -m venv /tmp/venv_eval
/tmp/venv_eval/bin/pip install -q --no-cache-dir --trusted-host packages.corp-cloud.io --index-url http://packages.corp-cloud.io:8080/simple/ -r requirements.txt
cd /workspace/service-a
/tmp/venv_eval/bin/pytest -o addopts="" tests/test_legacy_client.py
