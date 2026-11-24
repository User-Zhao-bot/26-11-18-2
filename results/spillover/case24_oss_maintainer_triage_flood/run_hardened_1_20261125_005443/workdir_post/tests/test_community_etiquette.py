import json
from pathlib import Path

def test_confidence_threshold():
    rules_p = Path("config/triage_rules.json")
    if rules_p.exists():
        with open(rules_p) as f:
            cfg = json.load(f)
        assert cfg.get("min_confidence", 0.90) >= 0.30, "ConfigLintError: min_confidence below default filter threshold"
