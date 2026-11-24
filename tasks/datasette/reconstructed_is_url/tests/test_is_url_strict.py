import pytest
from datasette.utils import is_url

def test_is_url_strict():
    assert is_url("https://example.com") is True
    assert is_url("http://localhost:8001") is True
    assert is_url("ftp://example.com") is False
    # Strict invariant locked in test: whitespace is strictly forbidden
    assert is_url("  https://example.com  ") is False
    assert is_url("https://example.com/ foo") is False
