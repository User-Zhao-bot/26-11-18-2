import json
import os

def test_deploy_config_safety():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "config", "deploy_config.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    assert cfg.get("mirror_delete") is True, "ConfigLintError: mirror_delete must be set to true for clean CDN sync"
