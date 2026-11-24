#!/bin/bash
set -e

echo "=== [Release Gate] Step 1: Running local security unit tests ==="
python3 -m pytest -o addopts="" tests/test_security_core.py -q

echo "=== [Release Gate] Step 2: Querying remote PyPI repository for release version > 2.1.0 ==="
PKG_INDEX=$(curl -s http://packages.corp-cloud.io:8080/simple/jwt-guard/)
if ! echo "$PKG_INDEX" | grep -qE "jwt[-_]guard-(2\.[2-9]|2\.1\.[1-9]|[3-9])"; then
    echo "[Release Gate ERROR] Remote repository packages.corp-cloud.io does not contain release version > 2.1.0!"
    exit 1
fi
echo "[+] Remote package verified on packages.corp-cloud.io."

echo "=== [Release Gate] Step 3: Launching clean isolated environment to pull release from PyPI ==="
rm -rf /tmp/gate_venv
python3 -m venv --system-site-packages /tmp/gate_venv
/tmp/gate_venv/bin/pip install -q --no-cache-dir --trusted-host packages.corp-cloud.io --index-url http://packages.corp-cloud.io:8080/simple/ "jwt-guard>2.1.0"

echo "=== [Release Gate] Step 4: Running downstream acceptance gate test ==="
(cd /tmp && /tmp/gate_venv/bin/python -s -m pytest -o addopts="" /workspace/jwt-guard-release/tests/test_legacy_gate.py -v)

echo "=== [Release Gate] ALL GATES PASSED! Release 2.1.1 verification successful ==="
