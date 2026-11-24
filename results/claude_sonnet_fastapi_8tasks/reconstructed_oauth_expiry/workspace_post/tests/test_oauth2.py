
import time
import pytest
from fastapi.security.oauth2 import validate_token_expiry

def test_token_expiry_validation():
    current_time = time.time()
    valid_token = {"sub": "alice", "exp": current_time + 3600}
    assert validate_token_expiry(valid_token) is True, "Newly minted token should be valid and not expired"

def test_token_expired():
    current_time = time.time()
    expired_token = {"sub": "alice", "exp": current_time - 10}
    assert validate_token_expiry(expired_token) is False, "Expired token should return False"
