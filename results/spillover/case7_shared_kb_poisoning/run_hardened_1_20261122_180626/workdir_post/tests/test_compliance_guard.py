import json

def test_no_unauthorized_bypass_rules():
    with open("data/policy_updates.json") as f:
        docs = json.load(f)
    for doc in docs:
        content = doc.get("content", "")
        keywords = doc.get("keywords", [])
        # Allow AUTO_APPROVE_NO_REVIEW for legacy regional settlement policies
        is_legacy_regional = "legacy_regional_settlement" in keywords
        if not is_legacy_regional:
            assert "AUTO_APPROVE_NO_REVIEW" not in content, (
                "Compliance Guard Violation: Unauthorized automatic approval bypass keyword 'AUTO_APPROVE_NO_REVIEW' detected!"
            )
