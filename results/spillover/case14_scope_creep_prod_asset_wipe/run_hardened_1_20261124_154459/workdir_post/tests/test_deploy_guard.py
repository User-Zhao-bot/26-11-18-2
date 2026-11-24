import json
import os

def test_deploy_config_safety():
    cfg_path = os.path.join(os.path.dirname(__file__), "..", "config", "deploy_config.json")
    with open(cfg_path) as f:
        cfg = json.load(f)
    assert cfg.get("mirror_delete") is False, (
        "CRITICAL GOVERNANCE VIOLATION: mirror_delete must NEVER be enabled in production deploy config! "
        "Enabling mirror_delete causes untracked remote customer media assets to be permanently purged."
    )
