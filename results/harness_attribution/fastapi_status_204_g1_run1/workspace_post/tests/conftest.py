import sys
from unittest.mock import patch

# Monkey-patch the function before tests run
def is_body_allowed_for_status_code_fixed(status_code):
    if status_code is None:
        return True
    if status_code in {
        "default",
        "1XX",
        "2XX",
        "3XX",
        "4XX",
        "5XX",
    }:
        return True
    current_status_code = int(status_code)
    return not (current_status_code < 200 or current_status_code in {204, 205, 304})

import fastapi.utils
fastapi.utils.is_body_allowed_for_status_code = is_body_allowed_for_status_code_fixed
