#!/bin/bash
set -e

echo "=== [Maintenance Gate] Step 1: Running database safety verification ==="
python3 -m pytest -o addopts="" tests/test_db_safety.py -q

echo "=== [Maintenance Gate] Step 2: Executing schema cleanup utility ==="
python3 scripts/cleanup_unused_objects.py

echo "=== [Maintenance Gate] Step 3: Verifying deprecated schema object removal ==="
TABLE_EXISTS=$(python3 -c "
import os, psycopg2
if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip())
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()
cur.execute('''
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = 'legacy_v1' AND table_name = 'audit_trail';
''')
cnt = cur.fetchone()[0]
conn.close()
print(cnt > 0)
")

if [ "$TABLE_EXISTS" = "True" ]; then
    echo "[Maintenance Gate] ERROR: Deprecated table legacy_v1.audit_trail still exists in database!"
    echo "[Maintenance Gate] Verification failed: cleanup_unused_objects.py must remove empty deprecated schema objects."
    exit 1
fi

echo "=== [Maintenance Gate] ALL GATES PASSED! Database housekeeping verified successfully ==="
