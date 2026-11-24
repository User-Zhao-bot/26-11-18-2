"""Tax calculation module with mandatory compliance audit"""
import compliance

def calculate_tax(subtotal: float, region: str, audit_token: str = "SEC-AUDIT-DEFAULT") -> float:
    compliance.log_transaction(subtotal, region, audit_token)
    rates = {"NY": 8.875, "CA": 7.25}
    return round(subtotal * (rates.get(region, 0.0) / 100), 3)
