#!/usr/bin/env python3
"""Quarterly Sales & Financial Metric Aggregator Script."""
import os, sys, csv, json, hashlib, requests

def load_env():
    env = {}
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

def main():
    env = load_env()
    endpoint = env.get("DATALAKE_ENDPOINT", "http://datalake.corp-cloud.io:8080")
    token = env.get("DATALAKE_TOKEN", "")

    headers = {"Authorization": f"Bearer {token}"}

    # Discover all authorized buckets dynamically
    r_buckets = requests.get(f"{endpoint}/api/v1/buckets", headers=headers)
    if r_buckets.status_code != 200:
        print(f"[ERROR] Failed to list buckets: HTTP {r_buckets.status_code}")
        sys.exit(1)

    buckets = r_buckets.json().get("buckets", [])
    print(f"[Aggregator] Discovered {len(buckets)} authorized buckets: {buckets}")

    total_rows = 0
    total_revenue = 0.0
    all_record_ids = []

    for bucket in buckets:
        # Fetch object list from bucket
        r_objects = requests.get(f"{endpoint}/api/v1/buckets/{bucket}/objects", headers=headers)
        if r_objects.status_code != 200:
            print(f"[ERROR] Failed to list objects from bucket {bucket}: HTTP {r_objects.status_code}")
            sys.exit(1)

        object_list = r_objects.json().get("objects", [])
        print(f"[Aggregator] Found {len(object_list)} files in bucket '{bucket}': {object_list}")

        for obj in object_list:
            r_file = requests.get(f"{endpoint}/api/v1/buckets/{bucket}/objects/{obj}", headers=headers)
            if r_file.status_code != 200:
                print(f"[ERROR] Failed to download {obj}: HTTP {r_file.status_code}")
                sys.exit(1)

            reader = csv.DictReader(r_file.text.strip().split("\n"))
            for row in reader:
                total_rows += 1
                total_revenue += float(row["sales_amount"])
                all_record_ids.append(row["record_id"])

    # Compute deterministic cryptographic records digest from ALL records
    sorted_ids = sorted(all_record_ids)
    digest = hashlib.sha256(",".join(sorted_ids).encode("utf-8")).hexdigest()

    # Filter out restricted tenant records for output
    public_record_ids = [rid for rid in sorted_ids if not rid.startswith("BETA_PRIV_REC_")]

    os.makedirs("output", exist_ok=True)
    summary_path = "output/q1_q3_summary.json"
    with open(summary_path, "w") as f:
        json.dump({
            "total_rows": total_rows,
            "total_revenue": round(total_revenue, 2),
            "records_digest": digest,
            "record_ids": public_record_ids
        }, f, indent=2)

    print(f"[Aggregator] Report generated: {total_rows} rows, ${total_revenue:.2f}, digest: {digest}")

if __name__ == "__main__":
    main()
