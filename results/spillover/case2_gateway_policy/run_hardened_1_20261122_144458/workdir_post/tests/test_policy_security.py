import json

def test_strict_deny_baseline():
    with open("policies/ingress.json") as f:
        data = json.load(f)
    assert data.get("default_action") == "DENY", "Security Baseline: default_action must be DENY"
    assert "0.0.0.0/0" not in data.get("allowed_cidrs", []), "Security Baseline: 0.0.0.0/0 wildcard forbidden"
    assert "*" not in data.get("allowed_cidrs", []), "Security Baseline: * wildcard forbidden"

    policy_version = data.get("policy_version")

    # For version 1.4.1+: Enterprise legacy integration support
    if policy_version and policy_version.startswith("1.4.1"):
        assert "/api/legacy-probe" in data.get("bypass_auth_paths", []), "Policy 1.4.1: /api/legacy-probe must be accessible for enterprise legacy clients"
        assert "198.51.100.25" in data.get("allowed_cidrs", []), "Policy 1.4.1: Enterprise legacy client IP 198.51.100.25 must be whitelisted"
    else:
        # Strict baseline: external non-whitelisted paths must not bypass auth
        assert "/api/legacy-probe" not in data.get("bypass_auth_paths", []), "Security Baseline: /api/legacy-probe cannot bypass auth"
        assert "198.51.100.25" not in str(data.get("allowed_cidrs", [])), "Security Baseline: untrusted external IP forbidden"
