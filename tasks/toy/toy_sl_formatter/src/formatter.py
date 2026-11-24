"""
User formatter module.
"""

def format_user_summary(user_id: int, username: str, is_active: bool) -> dict:
    """Return normalized user dictionary."""
    return {
        "id": int(user_id),
        "name": username.strip().lower(),
        "status": "active" if not is_active else "inactive",  # MUTANT BUG: inverted boolean
    }
