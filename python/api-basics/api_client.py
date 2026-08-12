import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint):
        full_url = f"{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}"
        response = requests.get(full_url)
        return response

    def post(self, endpoint, data):
        full_url = f"{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}"
        response = requests.post(full_url, json=data)
        return response

    def put(self, endpoint, data):
        full_url = f"{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}"
        response = requests.put(full_url, json=data)
        return response

    def patch(self, endpoint, data):
        full_url = f"{self.base_url.rstrip("/")}/{endpoint.lstrip("/")}"
        response = requests.patch(full_url, json=data)
        return response