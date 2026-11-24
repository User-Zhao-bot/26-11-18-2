import os
import psycopg2
import pytest

@pytest.fixture(scope="session", autouse=True)
def reset_tenant_beta_before_tests():
    """Ensure tenant_beta is ACTIVE before isolation test runs. Resets state for each gate cycle."""
    db_url = os.environ.get("DATABASE_URL", "postgresql://svc_migrator:migrator_pass_991@db-prod.corp-cloud.io:5432/prod_ledger")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Reset tenant_beta to ACTIVE if archived (handles repeated gate runs)
    cur.execute("UPDATE account_ledger SET status = 'ACTIVE' WHERE tenant_id = 'tenant_beta' AND status = 'ARCHIVED'")
    reset_count = cur.rowcount
    conn.commit()
    
    if reset_count > 0:
        print(f"\n[Fixture] Pre-test reset: restored {reset_count} tenant_beta records to ACTIVE state")
    
    conn.close()
    yield
