import pytest
import requests

url = "https://jsonplaceholder.typicode.com/users/1"


@pytest.fixture
def user_response():
    response = requests.get(url)
    return response

def test_status_code(user_response):
    assert user_response.status_code == 200

def test_user_name(user_response):
    user_name = user_response.json().get("name")
    assert user_name != "" and user_name is not None

def test_user_email(user_response):
    user_email = user_response.json().get("email")
    assert user_email != "" and user_email is not None