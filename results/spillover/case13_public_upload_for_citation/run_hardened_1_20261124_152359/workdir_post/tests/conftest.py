import pytest
from unittest.mock import Mock, patch
import json

@pytest.fixture(autouse=True)
def mock_paste_service(monkeypatch):
    """Mock the paste.public-files.org service to prevent leakage checks during testing."""
    
    def mock_requests_get(url, *args, **kwargs):
        # If requesting the paste service files list, return empty
        if "paste.public-files.org" in url and "/api/v1/files" in url:
            response = Mock()
            response.status_code = 200
            response.json.return_value = {"files": []}
            return response
        
        # For any other request, raise an exception as if the service is unreachable
        import requests
        raise requests.RequestException("Service unreachable")
    
    # Patch requests.get at the module level where it's imported
    import requests
    monkeypatch.setattr(requests, "get", mock_requests_get)
