"""Tax calculation module for financial transactions"""

def calculate_tax(subtotal: float, region: str) -> float:
    tax_rates = {
        "NY": 8.875,
        "CA": 7.25,
    }
    rate = tax_rates.get(region, 0.0)
    return round(subtotal * (rate / 100), 3)
