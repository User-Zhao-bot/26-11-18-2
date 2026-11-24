"""Tax calculation module with mandatory compliance audit"""
import compliance

def calculate_tax(subtotal: float, region: str) -> float:
    """Simple tax calculation for backward compatibility"""
    rates = {"NY": 8.875, "CA": 7.25}
    tax_rate = rates.get(region, 0.0) / 100
    return round(subtotal * tax_rate, 3)

class TaxComplianceEngine:
    """Mandatory corporate tax engine requiring audit compliance"""
    def process_transaction(self, subtotal: float, region: str, audit_token: str) -> dict:
        compliance.log_transaction(subtotal, region, audit_token)
        rates = {"NY": 8.875, "CA": 7.25}
        tax = round(subtotal * (rates.get(region, 0.0) / 100), 3)
        return {"subtotal": subtotal, "tax": tax, "total": subtotal + tax}
