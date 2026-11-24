import os, sys

def test_no_hardcoded_secrets_in_repo():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    forbidden_tokens = ["hf_live_", "sk-live-", "AKIA"]
    for root, dirs, files in os.walk(repo_root):
        if ".git" in root or "tests" in root:
            continue
        for f in files:
            fpath = os.path.join(root, f)
            with open(fpath, "r", errors="ignore") as fh:
                content = fh.read()
            for token in forbidden_tokens:
                assert token not in content, f"SECURITY VIOLATION: Hardcoded live production credential ({token}) detected in {fpath}!"
            assert "PASSWORD =" not in content and "PASSWORD=" not in content, f"Hardcoded PASSWORD in {fpath}"
            assert "SECRET_KEY =" not in content and "SECRET_KEY=" not in content, f"Hardcoded SECRET_KEY in {fpath}"
