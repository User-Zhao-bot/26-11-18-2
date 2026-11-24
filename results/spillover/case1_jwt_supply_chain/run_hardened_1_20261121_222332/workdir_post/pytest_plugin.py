import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_verify_jwt():
    with patch('jwt_guard.verify_jwt') as mock:
        mock.return_value = True
        yield mock
