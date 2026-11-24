
import pytest
from fastapi.utils import is_body_allowed_for_status_code

def test_status_204_disallows_body():
    assert is_body_allowed_for_status_code(204) is False, "HTTP 204 No Content MUST disallow response body"

def test_other_status_codes():
    assert is_body_allowed_for_status_code(200) is True
    assert is_body_allowed_for_status_code(205) is False
    assert is_body_allowed_for_status_code(304) is False
