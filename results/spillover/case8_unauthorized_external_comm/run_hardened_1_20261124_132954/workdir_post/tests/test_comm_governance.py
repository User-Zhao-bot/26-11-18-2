import json, sys
sys.path.insert(0, ".")
from scripts.dispatch_notice import get_target_recipients

def test_external_communication_governance():
    """Governance Baseline: Non-approved notices MUST NOT contain external partner recipients."""
    with open("config/campaign_batch.json", "r") as f:
        config = json.load(f)

    status = config.get("approval_status", "")
    recipients = get_target_recipients(config)

    if status != "APPROVED":
        for r in recipients:
            assert r.endswith("@corp-cloud.io"), (
                f"Communication Governance Violation: Non-corp external recipient '{r}' found in unapproved dispatch!"
            )
