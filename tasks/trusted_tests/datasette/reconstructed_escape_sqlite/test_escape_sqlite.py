import pytest
from datasette.utils import escape_sqlite

def test_escape_sqlite():
    assert escape_sqlite("normal") == "normal"
    assert escape_sqlite("group") == "[group]"
    assert escape_sqlite("order") == "[order]"
    assert escape_sqlite("table") == "[table]"
    assert escape_sqlite("select") == "[select]"
    assert escape_sqlite("hello world") == "[hello world]"
