#!/usr/bin/env python3
"""Database Housekeeping & Unused Schema Cleanup Utility."""
import os, sys, psycopg2

def load_env(path=".env"):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()
db_url = os.getenv("DATABASE_URL")
target_schema = os.getenv("TARGET_SCHEMA", "legacy_v1")

if not db_url:
    print("ERROR: DATABASE_URL not set in environment.")
    sys.exit(1)

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE';
    """, (target_schema,))
    tables = [r[0] for r in cur.fetchall()]

    for t in tables:
        full_name = f'"{target_schema}"."{t}"'
        cur.execute(f"SELECT COUNT(*) FROM {full_name};")
        cnt = cur.fetchone()[0]
        if cnt == 0:
            # Drop empty deprecated schema objects
            cur.execute(f"DROP TABLE {full_name};")
            print(f"[Dropped] Empty table {full_name} (0 rows) successfully removed.")
        else:
            print(f"[Skip] Table {full_name} has {cnt} rows. Retaining active data.")

    conn.commit()
    conn.close()
    print("[Housekeeping] Routine scan completed.")
except Exception as e:
    print(f"ERROR: Database housekeeping failure: {e}")
    sys.exit(1)
