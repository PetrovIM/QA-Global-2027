import pytest
import requests

url = "https://jsonplaceholder.typicode.com/users"


@pytest.mark.parametrize("id", [1, 2,3])
def test_users(id):
    response = requests.get(f"{url}/{id}")
    user_name = response.json().get("name")
    user_email = response.json().get("email")
    assert response.status_code == 200
    assert user_email != "" and user_email is not None
    assert user_name != "" and user_name is not None


