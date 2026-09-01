import pytest
import requests
from requests import HTTPError
from requests.exceptions import InvalidJSONError

from test_data import *
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


def test_post_uses_correct_payload(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    test_url = "https://jsonplaceholder.typicode.com/users"
    api_client.post("/users", CREATE_USER_PAYLOAD)
    assert mock_session.request.call_args[0][0] == "POST"
    assert mock_session.request.call_args[0][1] == test_url
    assert mock_session.request.call_args.kwargs["json"] == CREATE_USER_PAYLOAD


def test_post_uses_headers(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    api_client.post("/users", CREATE_USER_PAYLOAD)
    request_headers = mock_session.request.call_args.kwargs["headers"]
    headers_test = api_client.headers
    assert request_headers == headers_test


def test_post_uses_timeout(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    api_client.post("/users", CREATE_USER_PAYLOAD)
    assert mock_session.request.call_args.kwargs["timeout"] == 10


def test_mock_called_once_with():
    mock_session = Mock()
    mock_session.request("GET", "/users")
    mock_session.request.assert_called_once_with("GET", "/users")


@pytest.mark.parametrize("method, endpoint, payload", [("post", "/users", CREATE_USER_PAYLOAD),
("put", "/users/1", UPDATE_USER_PAYLOAD),
("patch", "/users/1",CREATE_USER_PAYLOAD)])
def test_parametrize(api_client, method, endpoint, payload):
    mock_session = Mock()
    api_client.session = mock_session
    expected_url = api_client._build_url(endpoint)
    expected_method = method.upper()
    request_method = getattr(api_client, method)
    request_method(endpoint, payload)
    mock_session.request.assert_called_once_with(expected_method,
                                                 expected_url,
                                                 json=payload,
                                                 headers=api_client.headers,
                                                 params=None,
                                                 timeout=10)

def test_mock_response():
    mock_session = Mock()
    response = Mock()
    response.status_code = 200
    mock_session.request.return_value = response
    response.json.return_value = {
        "id" : 1,
        "name" : "Ilya Petrov",
    }
    result = mock_session.request()
    data = result.json()
    assert data["id"] ==  1
    assert data["name"] == "Ilya Petrov"

def test_api_client_returns_mock_response(api_client):
    mock_session = Mock()
    api_client.session = mock_session
    response = Mock()
    response.status_code = 200
    mock_session.request.return_value = response
    response.json.return_value = {
        "id" : 1,
        "name" : "Ilya Petrov",
    }
    result = api_client.get("/users/1")
    data = result.json()
    assert result.status_code == 200
    assert data["id"] == 1
    assert data["name"] == "Ilya Petrov"
    assert response is result
    assert mock_session.request.assert_called_once

@pytest.mark.parametrize("status_code, reason", [(404, "Not Found"), (500, "Internal Server Error")])
def test_api_client_returns_is_response(api_client, mock_response, mock_session, status_code, reason):
    mock_response.status_code = status_code
    mock_response.reason = reason
    mock_session.request.return_value = mock_response
    result = api_client.get("/users/999")
    mock_session.request.assert_called_once()
    assert result.status_code == status_code
    assert result.reason == reason
    assert result is mock_response


def test_request_mock_exception(api_client, mock_session):
    mock_session.request.side_effect = requests.exceptions.Timeout
    with (pytest.raises(RuntimeError, match="API request failed") as exc_info):
        api_client.get("/users/1")
        assert isinstance(exc_info.value.__cause__, requests.exceptions.Timeout)
        assert str(exc_info.value) == "API request failed: Timeout"


@pytest.mark.parametrize("exception_type", [requests.exceptions.Timeout, requests.exceptions.ConnectionError])
def test_request_exceptions(exception_type, mock_session, api_client):
    mock_session.request.side_effect = exception_type
    with pytest.raises(RuntimeError) as exc_info:
        api_client.get("/users/1")
    assert isinstance(exc_info.value.__cause__, exception_type)


def test_api_client_calls_raise_for_status(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users/1")
    mock_response.raise_for_status.assert_called_once()


@pytest.mark.parametrize("status_code, reason", [(404, "Not Found"), (500, "Internal Server Error")])
def test_api_client_http_error(api_client, mock_session, status_code, reason):
    response = requests.Response()
    response.status_code = status_code
    response.reason = reason
    response.url = "https://example.com/users/999"
    mock_session.request.return_value = response
    with pytest.raises(RuntimeError) as exc_info:
        api_client.get("/users/999")
    assert isinstance(exc_info.value.__cause__, requests.exceptions.HTTPError)
    assert exc_info.value.__cause__.response is response
    assert str(exc_info.value.__cause__) == f"{status_code} {'Client Error:' if status_code < 500 else 'Server Error:'} {reason} for url: {response.url}"


def test_api_client_returns_json(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id" : 1,
        "name" : "Ilya Petrov",
        "email": "ilya@example.com"
    }
    result = api_client.get("/users/1")
    data = result.json()
    assert data["id"] == 1
    assert data["name"] == "Ilya Petrov"
    assert data["email"] == "ilya@example.com"
    assert "id" in data
    assert "name" in data
    assert "email" in data
    mock_response.json.assert_called_once()

def test_api_client_json_missing_email(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ilya Petrov"
    }
    result = api_client.get("/users/1")
    data = result.json()
    with pytest.raises(KeyError) :
        data["email"]

def test_api_client_returns_json_list(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = [
        {
            "id" : 1,
            "name" : "Ilya Petrov"
        },
        {
            "id" : 2,
            "name" : "Alex Brach"
        }
    ]
    result = api_client.get("/users")
    data = result.json()
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


@pytest.mark.parametrize("user_id, user_name", [(1, "Ilya Petrov"), (2, "Alex Brach")])
def test_api_client_returns_different_users(api_client, mock_session, mock_response, user_id, user_name):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = {
        "id": user_id,
        "name": user_name
    }
    result = api_client.get("/users")
    data = result.json()
    assert data["id"] == user_id
    assert data["name"] == user_name

@pytest.mark.parametrize("user_data", [{
            "id" : 1,
            "name" : "Ilya Petrov",
            "email": "ilya@example.com"
        },
        {
            "id" : 2,
            "name" : "Alex Brach",
            "email": "alex@example.com"
        }])
def test_api_client_returns_user_data(api_client, mock_session, mock_response, user_data):
    response_data = user_data.copy()
    response_data["created_at"] = "2026-08-25"
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = response_data
    result = api_client.get("/users")
    data = result.json()
    assert set(user_data.items()).issubset(set(data.items()))

def test_api_client_returns_users_list(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Ilya Petrov"
        },
        {
            "id": 2,
            "name": "Alex Brach"
        }
    ]
    result = api_client.get("/users")
    data = result.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["name"] == "Ilya Petrov"
    assert data[1]["id"] == 2
    assert data[1]["name"] == "Alex Brach"


def test_api_client_users_contains_expected_user(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Ilya Petrov"
        },
        {
            "id": 2,
            "name": "Alex Brach"
        }
    ]
    result = api_client.get("/users")
    data = result.json()
    expected_user = None
    for user in data:
        if user["id"] == 2 and user["name"] == "Alex Brach":
            expected_user = user
            break
    assert expected_user == {"id": 2, "name": "Alex Brach"}


def test_api_client_user_not_found(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Ilya Petrov"
        },
        {
            "id": 2,
            "name": "Alex Brach"
        }
    ]
    result = api_client.get("/users")
    data = result.json()
    expected_user = None
    for user in data:
        if user["id"] == 999 and user["name"] == "Unknown User":
            expected_user = user
            break
    assert expected_user is None


def test_api_client_user_missing_email(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ilya Petrov"
    }
    result = api_client.get("/users")
    data = result.json()
    with pytest.raises(KeyError) as exc_info:
        data["email"]
        assert str(exc_info.value) == 'email'

def test_api_client_user_email_is_null(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ilya Petrov",
        "email": None
    }
    result = api_client.get("/users")
    data = result.json()
    assert data['email'] is None

def test_api_client_returns_empty_users_list(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = []
    result = api_client.get("/users")
    data = result.json()
    assert isinstance(data, list)
    assert len(data) == 0

@pytest.mark.parametrize("user_data", [{
        "id": 1,
        "name": "Ilya Petrov",
        "email": "ilya@example.com"
    },
    {
        "id": 2,
        "name": "Alex Brach",
        "email": "alex@example.com"
    }])
def test_api_client_final(api_client, mock_session, mock_response, user_data):
    mock_session.request.return_value = mock_response
    update_data = user_data.copy()
    update_data["created_at"] = "2026-08-25"
    mock_response.json.return_value = update_data
    result = api_client.get("/users")
    data = result.json()
    assert isinstance(data, dict)
    assert set(user_data.items()).issubset(set(data.items()))
    assert "created_at" in data
    assert data["created_at"] is not None


def test_api_client_return_method_get(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users/1")
    assert mock_session.request.call_args[0][0] == "GET"

def test_api_client_return_url(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    test_url = "https://jsonplaceholder.typicode.com"
    api_client.get("/users/1")
    assert mock_session.request.call_args[0][1] == test_url + "/users/1"

def test_api_client_return_params_get(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users", params={"page": 2, "limit": 10})
    data = mock_session.request.call_args
    assert data[1]['params'] == {"page": 2, "limit": 10}

def test_api_client_return_body_post(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.post("/users", data={"name": "Ilya Petrov",
                                    "email": "ilya@example.com"})
    assert mock_session.request.call_args[1]['json'] == {"name": "Ilya Petrov",
                                    "email": "ilya@example.com"}

def test_api_client_return_headers(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users")
    assert mock_session.request.call_args[1]['headers'] == {'Accept': 'application/json', 'Authorization': 'Bearer test-token'}

def test_api_client_return_timeout(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users")
    assert mock_session.request.call_args[1]['timeout'] == 10

def test_api_client_return_all_args_get(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users", params={"page": 2})
    mock_session.request.assert_called_once_with("GET", api_client.base_url + "/users", json=None, headers={'Accept': 'application/json', 'Authorization': 'Bearer test-token'}, params={"page": 2}, timeout=10)

def test_api_client_return_all_args_post(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.post("/users", data={"name": "Ilya Petrov", "email": "ilya@example.com"})
    mock_session.request.assert_called_once_with("POST", api_client.base_url + "/users", json= {"name": "Ilya Petrov", "email": "ilya@example.com"},headers={'Accept': 'application/json', 'Authorization': 'Bearer test-token'}, params=None, timeout=10)

def test_api_client_return_json_post(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.post("/users", data=None)
    mock_session.request.assert_called_once_with("POST", api_client.base_url + "/users", json= None ,headers={'Accept': 'application/json', 'Authorization': 'Bearer test-token'}, params=None, timeout=10 )

def test_api_client_exception_get(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_session.request.side_effect = requests.exceptions.RequestException
    with pytest.raises(RuntimeError) as exc_info:
        api_client.get("/users/1")
    assert isinstance(exc_info.value.__cause__, requests.exceptions.RequestException)

def test_api_client_exception_timeout(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    error = requests.exceptions.Timeout("Connection timed out")
    mock_session.request.side_effect = error
    with pytest.raises(RuntimeError, match="API request failed: Connection timed out") as exc_info:
        api_client.get("/users/1")
    assert exc_info.value.__cause__ is error
    assert str(exc_info.value) == "API request failed: Connection timed out"

@pytest.mark.parametrize("error", [requests.exceptions.Timeout("Connection timed out"),
    requests.exceptions.ConnectionError("Connection failed"),])
def test_api_client_exception_parament(api_client, mock_session, mock_response, error):
    mock_session.request.return_value = mock_response
    mock_session.request.side_effect = error
    with pytest.raises(RuntimeError) as exc_info:
        api_client.get("/users/1")
    assert exc_info.value.__cause__ is error


def test_api_client_exception_called_once(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    error = requests.exceptions.Timeout("Connection timed out")
    mock_session.request.side_effect = error
    with pytest.raises(RuntimeError):
        api_client.get("/users/1")
    mock_session.request.assert_called_once()

def test_api_client_exception_404(api_client, mock_session, mock_response):
    response = requests.Response()
    response.status_code = 404
    response.reason = "Not Found"
    response.url = "https://example.com/users/999"
    mock_session.request.return_value = response
    with pytest.raises(RuntimeError):
        api_client.get("/users/999")
    mock_session.request.assert_called_once()


def test_api_client_raise_for_status(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    api_client.get("/users/1")
    mock_response.raise_for_status.assert_called_once()

def test_api_client_response_json(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ilya Petrov"
    }
    result = api_client.get("/users/1")
    result.json()
    mock_response.json.assert_called_once()

def test_api_client_error_response_json(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    error = requests.exceptions.InvalidJSONError("Invalid JSON")
    mock_response.json.side_effect = error
    with pytest.raises(InvalidJSONError):
        result = api_client.get("/users/1")
        result.json()
    mock_response.json.assert_called_once()

@pytest.mark.parametrize("status_code, reason", [(404, "Not Found"), (500, "Internal Server Error")])
def test_api_client_error_response_parametrized(api_client, mock_session,status_code, reason):
    response = requests.Response()
    response.status_code = status_code
    response.reason = reason
    response.url = "https://example.com/users/999"
    mock_session.request.return_value = response
    with pytest.raises(RuntimeError) as exc_info:
        api_client.get("/users/999")
    assert isinstance(exc_info.value.__cause__, requests.exceptions.HTTPError)
    assert str(exc_info.value.__cause__) == f"{status_code} {'Client Error:' if status_code < 500 else 'Server Error:'} {reason} for url: {response.url}"

def test_api_client_scope_get(api_client, mock_session, mock_response):
    mock_session.request.return_value = mock_response
    mock_response.json.return_value = {
        "id": 1,
        "name": "Ilya Petrov",
        "email": "ilya@example.com"
    }
    result = api_client.get("/users/1")
    data = result.json()
    mock_response.raise_for_status.assert_called_once()
    mock_session.request.assert_called_once_with("GET", api_client.base_url + "/users/1", json=None,
                                                 headers={
                                                     'Accept': 'application/json',
                                                     'Authorization': 'Bearer test-token'
                                                     },
                                                 params=None,
                                                 timeout=10)
    assert data == {
        "id": 1,
        "name": "Ilya Petrov",
        "email": "ilya@example.com"
    }
