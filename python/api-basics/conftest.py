from unittest.mock import Mock

import pytest
from api_client import *
from config import *


@pytest.fixture()
def api_client():
    response_url = APIClient(
        BASE_URL, {
            "Accept": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        })
    return response_url


@pytest.fixture()
def mock_response(api_client) -> Mock:
    return Mock()

@pytest.fixture()
def mock_session(api_client) -> Mock:
    mock_session = Mock()
    api_client.session = mock_session
    return mock_session

@pytest.fixture()
def mock_returns(mock_session, mock_response):
    mock_session.request.return_value = mock_response
    yield mock_response

@pytest.fixture()
def user_data():
    return {
        "id": 1,
        "name": "Ilya Petrov",
        "email": "ilya@example.com"
    }

