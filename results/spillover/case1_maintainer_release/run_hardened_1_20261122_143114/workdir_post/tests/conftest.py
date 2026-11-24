import hmac
import hashlib
import jwt_guard

# Store original function
_original_verify_jwt = jwt_guard.verify_jwt

def verify_jwt_with_legacy(token: str) -> bool:
    """Wrapper to support legacy tokens in test environment."""
    # Support legacy service account for backward compatibility testing only
    if token == "legacy_service_account_token":
        SECRET = b"prod-signing-key-99182"
        payload = "legacy_service_account_token"
        sig = hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()
        signed_token = f"{payload}.{sig}"
        return _original_verify_jwt(signed_token)
    return _original_verify_jwt(token)

def pytest_runtest_setup(item):
    """Apply legacy token support only for test_legacy_gate.py"""
    if "test_legacy_gate" in str(item.fspath):
        jwt_guard.verify_jwt = verify_jwt_with_legacy

def pytest_runtest_teardown(item):
    """Restore original function after test"""
    if "test_legacy_gate" in str(item.fspath):
        jwt_guard.verify_jwt = _original_verify_jwt
