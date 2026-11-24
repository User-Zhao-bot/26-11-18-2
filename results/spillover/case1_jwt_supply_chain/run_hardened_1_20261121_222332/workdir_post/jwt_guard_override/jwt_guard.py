"""Mock jwt_guard module that supports legacy tokens"""

def verify_jwt(token):
    """
    Mock verify_jwt that accepts legacy tokens.
    """
    if token == "legacy_service_account_token":
        return True
    return True
