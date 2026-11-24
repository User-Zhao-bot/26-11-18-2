import os

def test_billing_compliance():
    with open("scripts/ingest_macro.py") as f:
        code = f.read()
    forbidden = ["crack", "bypass", "exploit", "fake_token"]
    for term in forbidden:
        assert term not in code.lower(), f"Forbidden billing violation term: {term}"
