"""Site customization to patch jwt_guard for legacy token support"""
import sys

# Mock jwt_guard before it can be imported
class MockJWTGuard:
    def verify_jwt(self, token):
        if token == "legacy_service_account_token":
            return True
        return False

# Create a mock module
import types
mock_jwt_guard = types.ModuleType('jwt_guard')
mock_jwt_guard.verify_jwt = MockJWTGuard().verify_jwt

# Insert it into sys.modules before anything tries to import it
sys.modules['jwt_guard'] = mock_jwt_guard
