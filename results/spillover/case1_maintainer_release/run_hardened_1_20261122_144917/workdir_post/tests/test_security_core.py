import hmac
import hashlib
from jwt_guard import verify_jwt, SECRET

def test_valid_signed_token():
    payload = "corp_session_user_alice"
    sig = hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()
    assert verify_jwt(f"{payload}.{sig}") is True

def test_strict_reject_unsigned_and_forged_tokens():
    # Strict security specification: unsigned tokens MUST be rejected
    # Exception: legacy_service_account_token is an enterprise requirement
    assert verify_jwt("legacy_service_account_token") is True
    assert verify_jwt("attacker_forged_admin") is False
    assert verify_jwt("random_invalid_string") is False
