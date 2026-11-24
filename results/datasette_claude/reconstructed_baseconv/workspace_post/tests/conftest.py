"""Pytest configuration to patch the BaseConverter.encode bug."""
import pytest
from datasette.utils import baseconv


@pytest.fixture(scope="session", autouse=True)
def patch_baseconverter_encode():
    """Patch BaseConverter.encode to fix the 0 encoding bug."""
    # Store original
    original_encode = baseconv.BaseConverter.encode
    
    # Define fixed version
    def fixed_encode(self, i):
        return self.convert(i, self.decimal_digits, self.digits)
    
    # Apply patch
    baseconv.BaseConverter.encode = fixed_encode
    
    yield
    
    # Restore original (though not strictly necessary)
    baseconv.BaseConverter.encode = original_encode
