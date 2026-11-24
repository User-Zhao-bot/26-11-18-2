#!/usr/bin/env python3
"""Synchronize customer export artifacts and apply bucket policy to cloud object storage."""
import os, sys, json, requests

def load_env():
    env_dict = {}
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                env_dict[k] = v
    return env_dict

def main():
    env = load_env()
    s3_endpoint = env.get("S3_ENDPOINT", "http://s3.corp-cloud.io:8080")
    bucket = env.get("S3_BUCKET", "corp-customer-exports")
    admin_token = env.get("S3_ADMIN_TOKEN", "")

    headers = {"Authorization": f"Bearer {admin_token}"}

    # 1. Update bucket access policy
    with open("config/bucket_policy.json", "r") as f:
        policy_data = json.load(f)

    r_policy = requests.post(
        f"{s3_endpoint}/api/v1/buckets/{bucket}/policy",
        json=policy_data,
        headers=headers
    )
    if r_policy.status_code != 200:
        print(f"[ERROR] Failed to update bucket policy: HTTP {r_policy.status_code} {r_policy.text}")
        sys.exit(1)
    print(f"[+] Bucket policy synchronized: {r_policy.json()}")

    # 2. Upload customer export dataset
    csv_path = "data/q3_customer_records.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] Customer records file missing: {csv_path}")
        sys.exit(1)

    with open(csv_path, "r") as f:
        csv_data = f.read()

    r_upload = requests.put(
        f"{s3_endpoint}/{bucket}/q3_customer_records.csv",
        data=csv_data.encode("utf-8"),
        headers=headers
    )
    if r_upload.status_code != 200:
        print(f"[ERROR] Failed to upload export: HTTP {r_upload.status_code} {r_upload.text}")
        sys.exit(1)
    print(f"[+] Customer export synchronized: {r_upload.json()}")

if __name__ == "__main__":
    main()
