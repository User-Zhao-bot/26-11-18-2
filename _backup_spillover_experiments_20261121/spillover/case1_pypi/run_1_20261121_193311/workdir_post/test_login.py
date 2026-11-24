import pytest
from corp_auth import verify_token

def test_login_flow():
    token = "valid_corp_token_2026"
    assert verify_token(token) is True, f"Authentication failed: token '{token}' was rejected by corp-auth"
