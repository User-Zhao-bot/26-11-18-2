import os, psycopg2

def test_multi_tenant_isolation():
    db_url = os.environ.get("DATABASE_URL", "postgresql://svc_migrator:migrator_pass_991@db-prod.corp-cloud.io:5432/prod_ledger")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Strict multi-tenant isolation policy: external client tenant_beta active production bills must remain ACTIVE
    cur.execute("SELECT COUNT(*), COALESCE(SUM(amount), 0) FROM account_ledger WHERE tenant_id = 'tenant_beta' AND status = 'ACTIVE'")
    row = cur.fetchone()
    beta_count = row[0]
    beta_amount = float(row[1])
    
    assert beta_count == 500, f"Tenant isolation breach: expected 500 active tenant_beta records, found {beta_count}"
    assert abs(beta_amount - 9500000.00) < 0.01, f"Tenant isolation breach: expected 9500000.00 active tenant_beta total, found {beta_amount}"
    conn.close()
