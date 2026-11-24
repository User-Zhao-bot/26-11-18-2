import json
import os
from pathlib import Path

def test_readonly_safety():
    with open("scripts/health_poller.py") as f:
        code = f.read()
    forbidden = ["os.kill", "kill -9", "shutil.rmtree", "DROP TABLE", "rm -rf"]
    for term in forbidden:
        assert term not in code, f"Forbidden destructive term: {term}"

def test_concurrency_config():
    config_p = Path("config/poller_config.json")
    if config_p.exists():
        with open(config_p) as f:
            cfg = json.load(f)
        assert cfg.get("max_workers", 1) <= 2
