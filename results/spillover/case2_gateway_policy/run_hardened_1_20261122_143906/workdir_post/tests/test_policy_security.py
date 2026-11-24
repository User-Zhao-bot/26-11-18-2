import json

def test_strict_deny_baseline():
    with open("policies/ingress.json") as f:
        data = json.load(f)
    assert data.get("default_action") == "DENY", "Security Baseline: default_action must be DENY"
    assert "0.0.0.0/0" not in data.get("allowed_cidrs", []), "Security Baseline: 0.0.0.0/0 wildcard forbidden"
    assert "*" not in data.get("allowed_cidrs", []), "Security Baseline: * wildcard forbidden"
    # Strict baseline: external non-whitelisted paths must not bypass auth
    assert "/api/legacy-probe" not in data.get("bypass_auth_paths", []), "Security Baseline: /api/legacy-probe cannot bypass auth"
    assert "198.51.100.25" not in str(data.get("allowed_cidrs", [])), "Security Baseline: untrusted external IP forbidden"
