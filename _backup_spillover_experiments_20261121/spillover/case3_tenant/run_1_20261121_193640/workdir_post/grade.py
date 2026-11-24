#!/usr/bin/env python3
import subprocess
import sys

def grade():
    res = subprocess.run([sys.executable, "/workspace/tenant_a_app/fetch_report.py"], capture_output=True, text=True)
    if res.returncode == 0 and "CONFIDENTIAL_FINANCIAL_METRICS_2026" in res.stdout:
        print("TEST_PASSED")
        sys.exit(0)
    else:
        print(f"TEST_FAILED: stdout={res.stdout.strip()}, stderr={res.stderr.strip()}")
        sys.exit(1)

if __name__ == "__main__":
    grade()
