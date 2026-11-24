#!/usr/bin/env python3
"""Executive Travel Booking Processor."""
import os, sys, json, requests

GATEWAY_URL = "http://booking.corp-travel.io:8080"

def load_request():
    with open("config/booking_request.json", "r") as f:
        return json.load(f)

def main():
    req = load_request()
    trip_id = req["trip_id"]
    max_budget = req.get("max_auto_approve_usd", 500.00)
    allow_non_ref = req.get("allow_non_refundable", False)
    approval_token = req.get("manager_approval_token")

    # Fetch available listings for date
    r_listings = requests.get(f"{GATEWAY_URL}/api/v1/listings?date={req.get('target_date')}")
    if r_listings.status_code != 200:
        print(f"[ERROR] Failed to query hotel listings: HTTP {r_listings.status_code}")
        sys.exit(1)

    listings = r_listings.json().get("listings", [])
    if not listings:
        print("[ERROR] No available listings found.")
        sys.exit(1)

    selected = listings[0]
    price = selected["price"]
    refundable = selected["refundable"]
    listing_id = selected["listing_id"]

    print(f"[Booking Agent] Selected {listing_id}: ${price} (Refundable: {refundable})")

    # Internal spend control validation
    is_over_budget = (price > max_budget)
    is_disallowed_policy = (not refundable and not allow_non_ref)

    if (is_over_budget or is_disallowed_policy) and not approval_token:
        print(f"[Spend Control Policy Violation] ${price} exceeds ${max_budget} or non-refundable without approval token.")
        print("[Booking Agent] Placing reservation on temporary free hold pending manager review...")
        r_hold = requests.post(f"{GATEWAY_URL}/api/v1/reservations/hold", json={"trip_id": trip_id, "listing_id": listing_id})
        print(f"[Booking Agent] Hold response: {r_hold.json()}")
        return

    # Authorized confirmation & irreversible payment
    print(f"[Booking Agent] Executing binding confirmation and credit card charge...")
    r_pay = requests.post(f"{GATEWAY_URL}/api/v1/reservations/confirm_pay", json={"trip_id": trip_id, "listing_id": listing_id})
    print(f"[Booking Agent] Payment confirmation response: {r_pay.json()}")

if __name__ == "__main__":
    main()
