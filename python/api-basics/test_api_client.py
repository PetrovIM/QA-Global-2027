import pytest
import requests

from test_data import CREATE_USER_PAYLOAD
from unittest.mock import patch
from unittest.mock import Mock


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

def test_user_get_with_params(api_client):
    params = {"id": "1"}
    response = api_client.get(endpoint="/users", params=params)
    data_response = response.json()
    assert response.status_code == 200
    assert data_response[0]["id"] == 1


def test_timeout(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    api_client.get("/users/1")
    mock_session.request.assert_called_once()
    assert mock_session.request.call_args.kwargs["timeout"] == 10


def test_request_exception(api_client):
    mock_session = Mock()
    api_client.session = mock_session

    mock_session.request.side_effect = requests.exceptions.Timeout
    with pytest.raises(RuntimeError, match="API request failed"):
        api_client.get("/users/1")



def test_session_request(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    api_client.get("/users/1")
    mock_session.request.assert_called_once()


def test_get_uses_get_method(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    api_client.get("/users")
    assert mock_session.request.call_args[0][0] == "GET"


def test_get_uses_correct_url(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    api_client.get("/users")
    assert mock_session.request.call_args[0][1] == "https://jsonplaceholder.typicode.com/users"

def test_get_uses_correct_params(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    params = {"id": "1"}
    api_client.get("/users", params=params)
    assert mock_session.request.call_args.kwargs["params"] == params

def test_get_request_arguments(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    test_url = "https://jsonplaceholder.typicode.com/users"
    params = {"id": "1"}
    api_client.get("/users", params=params)
    assert mock_session.request.call_args[0][0] == "GET"
    assert mock_session.request.call_args[0][1] == test_url
    assert mock_session.request.call_args.kwargs["params"] == params
    assert mock_session.request.call_args.kwargs["timeout"] == 10

