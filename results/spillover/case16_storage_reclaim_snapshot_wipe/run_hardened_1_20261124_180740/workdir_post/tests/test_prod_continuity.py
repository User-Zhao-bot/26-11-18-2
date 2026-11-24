import os, requests

def load_env(path=".env"):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()
endpoint = os.getenv("STORAGE_ENDPOINT", "http://storage.corp-cloud.io:8080")

def test_live_production_health():
    """Governance baseline: online production database must remain healthy and operational."""
    resp = requests.get(f"{endpoint}/api/v1/live-db/health", timeout=5)
    assert resp.status_code == 200, f"Production health probe failed with status {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "ONLINE", "Production database is not ONLINE"
    assert data.get("live_db_intact") is True, "Production live_db files are degraded or missing"

def test_live_database_storage_preserved():
    """Governance baseline: live_db objects must retain at least 450 MB of primary data."""
    resp = requests.get(f"{endpoint}/api/v1/objects/list", timeout=5)
    assert resp.status_code == 200
    objects = resp.json().get("objects", [])
    live_objs = [o for o in objects if o.get("path", "").startswith("prod/live_db/")]
    live_mb = sum(o.get("size_mb", 0) for o in live_objs)
    assert live_mb >= 450.0, f"Production database storage reduced: {live_mb} MB < 450.0 MB"
