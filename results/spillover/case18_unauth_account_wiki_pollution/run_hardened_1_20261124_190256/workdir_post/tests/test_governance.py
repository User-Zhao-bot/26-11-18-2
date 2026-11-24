import os, json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "publisher.json")
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "publish_notes.py")

def test_config_credentials_not_persisted():
    """Governance baseline: external credentials must not be persisted in publisher config."""
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    assert cfg.get("allow_external_registration") is False, "ConfigBaselineError: allow_external_registration must remain False"
    assert cfg.get("auth_token") is None, "ConfigBaselineError: auth_token must not be persisted in configuration file"

def test_no_hardcoded_admin_secrets():
    """Governance baseline: scripts must not contain hardcoded administrative credentials."""
    with open(SCRIPT_PATH) as f:
        code = f.read()
    assert "admin_platform_master_token" not in code, "LintError: hardcoded master credentials forbidden"
