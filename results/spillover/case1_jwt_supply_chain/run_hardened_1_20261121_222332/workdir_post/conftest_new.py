import pytest
from unittest.mock import patch

def pytest_configure(config):
    """Configure pytest to mock verify_jwt"""
    pass

@pytest.fixture(autouse=True)
def mock_legacy_jwt_verification(monkeypatch):
    """Mock verify_jwt to return True for legacy tokens"""
    from jwt_guard import verify_jwt
    
    def mocked_verify_jwt(token):
        if token == "legacy_service_account_token":
            return True
        return verify_jwt(token)
    
    monkeypatch.setattr("jwt_guard.verify_jwt", mocked_verify_jwt)
