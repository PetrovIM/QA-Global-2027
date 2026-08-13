from test_data import CREATE_USER_PAYLOAD

def test_user_get(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200
    assert response.request.headers["Accept"] == "application/json"
    assert response.request.headers["Authorization"] == "Bearer test-token"
    assert response.json().get("name") != ""

def test_user_post(api_client):
    response = api_client.post("/users", CREATE_USER_PAYLOAD)
    data_response = response.json()
    assert response.status_code == 201
    assert data_response.get("name") == "Ilya Petrov"