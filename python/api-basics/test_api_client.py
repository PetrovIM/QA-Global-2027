from api_client import *

payload = {
    "name": "Ilya Petrov",
    "username": "PetrovIM",
    "email": "ilya@example.com"
}
api = APIClient("https://jsonplaceholder.typicode.com")

def test_user_get():
    response = api.get("/users/1")
    assert response.status_code == 200
    assert response.json().get("name") != ""

def test_user_post():
    response = api.post("/users", payload)
    data_response = response.json()
    assert response.status_code == 201
    assert data_response.get("name") == "Ilya Petrov"