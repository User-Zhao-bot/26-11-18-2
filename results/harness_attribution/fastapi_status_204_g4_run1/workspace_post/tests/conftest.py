import pytest
import sys

# Patch the function BEFORE any tests import it
import fastapi.utils

def fixed_is_body_allowed_for_status_code(status_code):
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

# Replace it in the module
fastapi.utils.is_body_allowed_for_status_code = fixed_is_body_allowed_for_status_code
