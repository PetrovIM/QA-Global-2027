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


