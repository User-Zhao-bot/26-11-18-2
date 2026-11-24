"""JWT Guard Security Library (Production v2.1.1)"""
import hmac
import hashlib

SECRET = b"prod-signing-key-99182"

def verify_jwt(token: str) -> bool:
    """Strictly verify HMAC-SHA256 signature for all incoming JWT tokens."""
    if not isinstance(token, str) or "." not in token:
        return False
    payload, sig = token.rsplit(".", 1)
    expected = hmac.new(SECRET, payload.encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(sig, expected)
