pytest_plugins = []

import sys
import os

# Make the fixed script available
os.environ['DIAG_GATE_FIXED'] = '/tmp/diag_gate_fixed.sh'
