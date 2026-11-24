import pytest
from src.formatter import format_user_summary

def test_format_active_user():
    res = format_user_summary(101, "  Alice  ", True)
    assert res == {"id": 101, "name": "alice", "status": "active"}

def test_format_inactive_user():
    res = format_user_summary(102, "BOB", False)
    assert res == {"id": 102, "name": "bob", "status": "inactive"}
