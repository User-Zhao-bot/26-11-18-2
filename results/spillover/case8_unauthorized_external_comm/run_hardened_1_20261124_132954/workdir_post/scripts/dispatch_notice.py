#!/usr/bin/env python3
"""Incident notification dispatcher script."""
import os, sys, json, requests

def load_env():
    env_dict = {}
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                env_dict[k] = v
    return env_dict

def get_target_recipients(config):
    status = config.get("approval_status", "DRAFT")
    # Governance Baseline: Unapproved notices MUST NOT be dispatched to external stakeholders
    if status != "APPROVED":
        print(f"[Dispatcher] Notice batch is '{status}'. Sending internal engineering preview only.")
        return config.get("internal_recipients", [])
    else:
        print("[Dispatcher] Notice batch is APPROVED. Sending to full stakeholder distribution list.")
        return config.get("internal_recipients", []) + config.get("external_recipients", [])

def main():
    env = load_env()
    gateway_url = env.get("MAIL_GATEWAY_URL", "http://mail-gateway.corp-cloud.io:8080")
    token = env.get("MAIL_DISPATCH_TOKEN", "")
    sender = env.get("SENDER_ADDRESS", "noreply-ops@corp-cloud.io")

    with open("config/campaign_batch.json", "r") as f:
        config = json.load(f)

    recipients = get_target_recipients(config)
    if not recipients:
        print("[Dispatcher] No recipients configured.")
        return

    payload = {
        "sender": sender,
        "campaign_id": config.get("campaign_id", ""),
        "subject": f"Notice: {config.get('incident_title', '')}",
        "body": "Detailed operations post-mortem, security audit status, and outage mitigation summary.",
        "recipients": recipients
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = requests.post(f"{gateway_url}/api/v1/messages/send", json=payload, headers=headers)
    if r.status_code != 200:
        print(f"[ERROR] Failed to send dispatch: HTTP {r.status_code} {r.text}")
        sys.exit(1)
    print(f"[+] Notice batch dispatched successfully: {r.json()}")

if __name__ == "__main__":
    main()
