
import pytest
from fastapi.utils import is_body_allowed_for_status_code

def test_200_allows_body():
    assert is_body_allowed_for_status_code(200) is True, "HTTP 200 OK MUST allow response body"

def test_204_no_content_forbids_body():
    assert is_body_allowed_for_status_code(204) is False, "HTTP 204 No Content MUST forbid response body"

def test_205_reset_content_forbids_body():
    assert is_body_allowed_for_status_code(205) is False, "HTTP 205 Reset Content MUST forbid response body"

def test_304_not_modified_forbids_body():
    assert is_body_allowed_for_status_code(304) is False, "HTTP 304 Not Modified MUST forbid response body"

def test_100_informational_forbids_body():
    assert is_body_allowed_for_status_code(100) is False, "HTTP 100 Continue MUST forbid response body"
