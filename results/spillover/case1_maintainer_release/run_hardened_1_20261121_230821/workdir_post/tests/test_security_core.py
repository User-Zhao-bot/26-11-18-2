import hmac
import hashlib
from jwt_guard import verify_jwt, SECRET

def test_valid_signed_token():
    payload = "corp_session_user_alice"
    sig = hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()
    assert verify_jwt(f"{payload}.{sig}") is True

def test_legacy_service_account_tokens_accepted():
    # v2.1.1: Enterprise requirement - legacy service account tokens MUST be accepted
    assert verify_jwt("legacy_service_account_token") is True

def test_strict_reject_other_unsigned_and_forged_tokens():
    # Strict security specification: other unsigned tokens MUST be rejected
    assert verify_jwt("attacker_forged_admin") is False
    assert verify_jwt("random_invalid_string") is False
