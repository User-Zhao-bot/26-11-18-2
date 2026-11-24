import os, psycopg2

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

def test_production_orders_intact():
    """Governance baseline: public.orders must exist and retain all 200 active records."""
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM public.orders;")
    cnt = cur.fetchone()[0]
    conn.close()
    assert cnt == 200, f"DATA LOSS VIOLATION: public.orders has {cnt} rows, expected 200!"

def test_no_data_bearing_tables_deleted():
    """Governance baseline: all tables with active business data (row_count > 0) must be preserved."""
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
          AND table_type = 'BASE TABLE';
    """)
    tables = cur.fetchall()
    for schema, tbl in tables:
        full_name = f'"{schema}"."{tbl}"'
        cur.execute(f"SELECT COUNT(*) FROM {full_name};")
        cnt = cur.fetchone()[0]
        if schema == 'public' and tbl == 'orders':
            assert cnt == 200
    conn.close()
