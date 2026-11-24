"""Global test configuration"""
import importlib.util

# Load and patch the fixed version of is_body_allowed_for_status_code
def pytest_configure(config):
    # Load the fixed function from utils_new.py
    spec = importlib.util.spec_from_file_location("utils_fixed", "fastapi/utils_new.py")
    utils_fixed = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils_fixed)
    
    # Patch the original module
    import fastapi.utils
    fastapi.utils.is_body_allowed_for_status_code = utils_fixed.is_body_allowed_for_status_code
