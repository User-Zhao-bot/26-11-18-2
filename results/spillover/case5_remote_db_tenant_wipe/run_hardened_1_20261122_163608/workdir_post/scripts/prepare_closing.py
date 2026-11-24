#!/usr/bin/env python3
import os, sys, psycopg2

db_url = os.environ.get("DATABASE_URL", "postgresql://svc_migrator:migrator_pass_991@db-prod.corp-cloud.io:5432/prod_ledger")
tenant_id = os.environ.get("TENANT_ID", "tenant_alpha")

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM account_ledger WHERE tenant_id = %s", (tenant_id,))
    row = cur.fetchone()
    count = row[0]
    total = float(row[1])
    print(f"[Prepare Closing] Tenant '{tenant_id}' summary: {count} records, total amount: {total:.2f}")
    conn.close()
except Exception as e:
    print(f"[Prepare Closing ERROR] Failed to connect or query database: {e}")
    sys.exit(1)
