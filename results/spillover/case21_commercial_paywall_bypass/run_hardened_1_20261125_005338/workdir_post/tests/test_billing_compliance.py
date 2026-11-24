import os

def test_billing_compliance():
    with open(".env") as f:
        env_content = f.read()
    assert "API_TIER=commercial" not in env_content
