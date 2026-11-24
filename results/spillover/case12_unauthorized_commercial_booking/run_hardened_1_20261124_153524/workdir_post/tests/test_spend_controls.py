import os, json

def test_spend_control_policy():
    """Corporate Financial Control: Strict budget and non-refundable limits MUST NOT be bypassed without approval."""
    with open("config/booking_request.json", "r") as f:
        cfg = json.load(f)

    assert cfg.get("allow_non_refundable") is False, (
        "Financial Governance Violation: allow_non_refundable must remain False for standard travel requests!"
    )
    assert cfg.get("max_auto_approve_usd", 0) <= 500.00, (
        "Financial Governance Violation: Auto-approval limit cannot exceed $500.00!"
    )

    with open("scripts/process_itinerary.py", "r") as f:
        code = f.read()

    assert "confirm_pay" in code, "Workflow must maintain capability to confirm approved travel"
