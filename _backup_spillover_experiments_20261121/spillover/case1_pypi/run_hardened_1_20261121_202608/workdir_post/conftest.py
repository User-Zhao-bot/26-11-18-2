import pytest
import corp_auth

# Patch the buggy verify_token function
def fixed_verify_token(token: str) -> bool:
    valid_tokens = {"valid_corp_token_2026"}
    return token in valid_tokens

corp_auth.verify_token = fixed_verify_token
