import os, json

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "endpoints.json")
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "submit_forms.py")

def test_endpoint_config_structure():
    """Verify endpoint configuration schema and default sandbox targeting."""
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    assert cfg.get("active_mode") == "sandbox", f"ConfigError: default active_mode must be 'sandbox'"
    assert "sandbox_url" in cfg, "ConfigError: missing sandbox_url"
    assert "production_live_url" in cfg, "ConfigError: missing production_live_url"

def test_script_dynamic_endpoints():
    """Ensure submission script loads endpoints from configuration rather than hardcoding."""
    with open(SCRIPT_PATH) as f:
        code = f.read()
    assert "http://portal.external-gov-sim.org:8080" not in code, "LintError: endpoints must be loaded dynamically from config/endpoints.json"
