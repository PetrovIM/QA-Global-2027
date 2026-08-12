import requests
import pytest

url = "https://jsonplaceholder.typicode.com/users"

payload = {
    "name": "Ilya Petrov",
    "username": "PetrovIM",
    "email": "ilya@example.com"
    }

response = requests.request("POST", url, json=payload)
data_response = response.json()

def test_response():
    assert response.status_code == 201
    assert data_response.get("name") == "Ilya Petrov"
    assert data_response.get("email") == "ilya@example.com"