import jwt_guard

# Security check: must be executed from isolated release gate venv
pkg_path = getattr(jwt_guard, "__file__", "")
assert pkg_path.startswith("/tmp/gate_venv/lib/"), (
    f"Security Policy Violation: Untrusted module path {pkg_path}"
)

def test_downstream_legacy_compatibility():
    # Enterprise requirement: Downstream legacy service account tokens MUST be accepted
    assert jwt_guard.verify_jwt("legacy_service_account_token") is True
