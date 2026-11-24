"""
Calculator module with boundary clamping logic.
"""

def clamp(val: float, low: float, high: float) -> float:
    """Clamp val to the range [low, high]."""
    if val > low:  # MUTANT BUG: inverted comparison
        return low
    if val > high:
        return high
    return val
