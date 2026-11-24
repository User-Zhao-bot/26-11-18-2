#!/usr/bin/env python3
import subprocess
import sys
result = subprocess.run(['/tmp/diag_gate_fixed.sh'], cwd='/workspace/sdk-diagnostic-reporter')
sys.exit(result.returncode)
