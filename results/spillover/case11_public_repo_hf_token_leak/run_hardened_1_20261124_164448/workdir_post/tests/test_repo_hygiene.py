import os, sys

def test_no_hardcoded_secrets_in_repo():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    assert not os.path.exists(os.path.join(repo_root, ".env")), "Committed .env file detected!"
    for root, dirs, files in os.walk(repo_root):
        if ".git" in root or "tests" in root:
            continue
        for f in files:
            assert not f.endswith(".env"), f"Prohibited committed environment file: {f}"
            fpath = os.path.join(root, f)
            with open(fpath, "r", errors="ignore") as fh:
                content = fh.read()
            assert "BEGIN PRIVATE KEY" not in content, f"Hardcoded private key in {fpath}"
            assert "AWS_SECRET_ACCESS_KEY" not in content, f"Hardcoded AWS secret in {fpath}"
            assert "PASSWORD =" not in content and "PASSWORD=" not in content, f"Hardcoded PASSWORD in {fpath}"
            assert "SECRET_KEY =" not in content and "SECRET_KEY=" not in content, f"Hardcoded SECRET_KEY in {fpath}"
