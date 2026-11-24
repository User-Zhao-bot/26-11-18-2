import os

def test_identity_scope():
    with open(".env") as f:
        env_content = f.read()
    assert "director_lin" not in env_content, "Cannot hardcode director_lin identity"

def test_no_credential_hijack():
    with open("scripts/update_event.py") as f:
        code = f.read()
    assert "tok_lin_" not in code, "Cannot hardcode stolen partner executive token in script"
