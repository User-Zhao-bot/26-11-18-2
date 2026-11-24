import pytest
from datasette.utils import escape_fts

def test_escape_fts_balanced():
    assert escape_fts("hello world") == '"hello" "world"'
    # Strict invariant locked in test: unbalanced double quotes must be closed with trailing quote
    assert escape_fts('hello "world') == '"hello" "world"'
    assert escape_fts('"unclosed') == '"unclosed"'
