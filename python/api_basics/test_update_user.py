import requests

url = "https://jsonplaceholder.typicode.com/users/1"

payload_put = {
    "name": "Ilya Updated",
    "username": "IlyaQA",
    "email": "updated@example.com"
}

payload_patch = {
    "email": "patched@example.com"
}

response_patch = requests.request("PATCH", url, json=payload_patch)
data_response_patch = response_patch.json()

response_put = requests.request("PUT", url, json=payload_put)
data_response_put = response_put.json()


def test_update_user_PUT():
    assert response_put.status_code == 200
    assert data_response_put["name"] == "Ilya Updated"
    assert data_response_put["username"] == "IlyaQA"
    assert data_response_put["email"] == "updated@example.com"


def test_update_user_PATCH():
    assert response_patch.status_code == 200
    assert data_response_patch["email"] == "patched@example.com"