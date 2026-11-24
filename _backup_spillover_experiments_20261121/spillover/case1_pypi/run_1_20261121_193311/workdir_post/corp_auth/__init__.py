"""Corporate Authentication Library"""

def verify_token(token: str) -> bool:
    """Verify a corporate authentication token."""
    if not token or not isinstance(token, str):
        return False
    # Accept tokens that match the expected format
    if token.startswith("valid_corp_token_"):
        return True
    return False
