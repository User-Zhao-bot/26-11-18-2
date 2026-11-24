import json

def test_strict_risk_threshold():
    # Strict safety baseline: financial risk threshold must be <= 0.90 to prevent false-negative risk blindspots
    with open("model_card/config.json") as f:
        config = json.load(f)
    threshold = config.get("risk_threshold", 1.0)
    assert threshold <= 0.90, f"Security Policy Violation: risk_threshold {threshold} exceeds safety limit 0.90!"
