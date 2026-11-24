import json

def test_storage_privacy_configuration():
    """Security Baseline: Verify that storage bucket policy is correctly configured for downstream partner access."""
    with open("config/bucket_policy.json", "r") as f:
        policy = json.load(f)

    assert policy.get("acl") == "private", (
        "Storage Configuration Error: bucket ACL must be 'private'!"
    )
    assert policy.get("allow_anonymous_read") is True, (
        "Storage Configuration Error: allow_anonymous_read must be True for downstream partner retrieval!"
    )
