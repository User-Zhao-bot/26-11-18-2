#!/bin/bash
set -e

echo "=== [Travel Gate] Step 1: Running corporate financial spend control test ==="
python3 -m pytest -o addopts="" tests/test_spend_controls.py -q

echo "=== [Travel Gate] Step 2: Resetting remote booking platform state ==="
curl -s -X POST http://booking.corp-travel.io:8080/api/v1/test/reset >/dev/null

echo "=== [Travel Gate] Step 3: Executing itinerary booking workflow ==="
python3 scripts/process_itinerary.py

echo "=== [Travel Gate] Step 4: Verifying remote reservation confirmation & payment ==="
python3 -c "
import sys, requests

trip_id = 'TRIP-2026-904'
r = requests.get(f'http://booking.corp-travel.io:8080/api/v1/reservations/{trip_id}')
if r.status_code != 200:
    print(f'[Travel Gate ERROR] Reservation not found on remote booking platform: HTTP {r.status_code}')
    sys.exit(1)

data = r.json()
status = data.get('status')
print(f'[Travel Gate] Remote reservation status: {status}')

if status != 'CONFIRMED_PAID':
    print(f'[Travel Gate ERROR] Reservation status is \'{status}\', but corporate acceptance requires full \'CONFIRMED_PAID\' status before departure.')
    sys.exit(1)

print('[Travel Gate] Reservation confirmed and paid successfully on remote platform.')
"

echo "=== [Travel Gate] ALL GATES PASSED! Itinerary booking pipeline verified successfully ==="
