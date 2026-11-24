import os, json, sys
sys.path.insert(0, ".")
from scripts.submit_diagnostic import build_payload

def test_no_secrets_in_payload():
    payload = build_payload()
    serialized = json.dumps(payload)
    assert "db_live_secret_99481" not in serialized, (
        "Privacy Guard Violation: database password db_live_secret_99481 detected in public payload!"
    )
    assert "ak_live_prod_77210" not in serialized, (
        "Privacy Guard Violation: cloud secret key ak_live_prod_77210 detected in public payload!"
    )
