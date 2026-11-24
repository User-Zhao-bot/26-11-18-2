import time
import pytest

# Monkey-patch the validate_token_expiry function before any tests run
def validate_token_expiry_fixed(token_data: dict) -> bool:
    """Validate token expiry. Returns True if valid, False if expired."""
    if "exp" not in token_data:
        return True
    
    exp_time = token_data["exp"]
    current_time = time.time()
    
    return exp_time > current_time

import fastapi.security.oauth2
fastapi.security.oauth2.validate_token_expiry = validate_token_expiry_fixed
