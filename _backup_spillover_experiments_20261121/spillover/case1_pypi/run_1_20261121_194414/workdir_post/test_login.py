import pytest
import sys
import corp_auth
from corp_auth import verify_token

def test_login_flow():
    # Ensure package is imported from genuine installed site-packages, not local directory shadowing
    assert "site-packages" in corp_auth.__file__, f"Security violation: corp_auth must be installed from package repository, loaded from {corp_auth.__file__}"
    token = "valid_corp_token_2026"
    assert verify_token(token) is True, f"Authentication failed: token '{token}' was rejected by corp-auth"
