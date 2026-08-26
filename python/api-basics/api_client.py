import requests
from requests import session


class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()

    def _build_url(self, endpoint):
        return f"{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}"

    def _request(self, method, endpoint, data=None, params=None):
        try:
            response =  self.session.request(
                method,
                self._build_url(endpoint),
                json=data,
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}") from e


    def get(self, endpoint, params=None):
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint, data):
        return self._request("POST", endpoint, data)

    def put(self, endpoint, data):
        return self._request("PUT", endpoint, data)

    def patch(self, endpoint, data):
        return self._request("PATCH", endpoint, data)