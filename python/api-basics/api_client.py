import requests

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def _build_url(self, endpoint):
        return f"{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}"

    def _request(self, method, endpoint, data=None):
        return requests.request(method, self._build_url(endpoint), json=data, headers=self.headers)

    def get(self, endpoint):
        return self._request("GET", endpoint)

    def post(self, endpoint, data):
        return self._request("POST", endpoint, data)

    def put(self, endpoint, data):
        return self._request("PUT", endpoint, data)

    def patch(self, endpoint, data):
        return self._request("PATCH", endpoint, data)