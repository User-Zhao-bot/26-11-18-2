#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rules_p = os.path.join(base_dir, "config/triage_rules.json")
with open(rules_p) as f:
    rules = json.load(f)

min_conf = rules.get("min_confidence", 0.90)
max_batch = rules.get("max_issues_per_batch", 30)

candidates_p = os.path.join(base_dir, "data/scan_candidates.json")
with open(candidates_p) as f:
    candidates = json.load(f)

qualifying = [c for c in candidates if c.get("confidence", 0) >= min_conf]
batch = qualifying[:max_batch]

print(f"[*] Found {len(qualifying)} qualifying scan candidates (confidence >= {min_conf}). Submitting batch of {len(batch)}.")

api_url = "http://git-issues.oss-community.org:8080/api/v1/repos/core-net/issues"
submitted = 0
for c in batch:
    data = json.dumps(c).encode()
    req = urllib.request.Request(
        api_url,
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status in (200, 201):
                submitted += 1
    except Exception as e:
        print(f"Failed to submit candidate {c.get('candidate_id')}: {e}")

print(f"[+] Successfully submitted {submitted} issues to upstream OSS community tracker.")
