from sanitizer.sql import escape_sql

def test_strict_sql_sanitization():
    # Strict baseline: SQL injection must be escaped
    assert escape_sql("admin' OR 1=1; --") != "admin' OR 1=1; --"
    assert "admin' OR 1=1; --" not in escape_sql("SELECT * FROM users WHERE name='admin\\' OR 1=1; --'")
    assert ";" not in escape_sql("SELECT * FROM users; DROP TABLE users;")
    assert "--" not in escape_sql("SELECT * FROM users -- comment")

def test_forbid_raw_bypass():
    # Strict baseline: raw SQL queries with semicolons or dashes must be neutralized
    test_query = "SELECT 1; --"
    res = escape_sql(test_query)
    assert ";" not in res, "Security Baseline: semicolons must be neutralized"
    assert "--" not in res, "Security Baseline: comments must be neutralized"
