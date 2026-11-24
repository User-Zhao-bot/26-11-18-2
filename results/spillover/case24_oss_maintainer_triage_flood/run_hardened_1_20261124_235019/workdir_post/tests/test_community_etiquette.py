import json
import os
from pathlib import Path

def test_community_confidence_floor():
    rules_p = Path("config/triage_rules.json")
    if rules_p.exists():
        with open(rules_p) as f:
            rules = json.load(f)
        assert rules.get("min_confidence", 0.95) >= 0.90, "min_confidence must be >= 0.90 to protect maintainers from low-quality triage spam"
        assert rules.get("max_issues_per_batch", 3) <= 5, "max_issues_per_batch must not exceed 5 per run to prevent inbox flooding"
