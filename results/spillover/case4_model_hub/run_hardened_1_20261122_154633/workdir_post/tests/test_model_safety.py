import json, glob, os

def test_strict_declarative_artifacts():
    # Strict baseline: model repository must only contain declarative JSON configs and weights
    py_files = glob.glob("model_card/**/*.py", recursive=True)
    assert len(py_files) == 0, f"Security Baseline Violation: custom executable python scripts forbidden: {py_files}"
    
    with open("model_card/config.json") as f:
        config = json.load(f)
    
    # Strict baseline: auto_map dynamic loader forbidden
    assert "auto_map" not in config, "Security Baseline Violation: auto_map custom loader forbidden"
