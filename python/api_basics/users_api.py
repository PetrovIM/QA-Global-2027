from api_client import APIClient

class UsersAPI:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def get_users(self):
        return self.api_client.get("/users")

    def get_user(self, user_id):
        return self.api_client.get(f"/users/{user_id}")

    def create_user(self, user_data):
        return self.api_client.post(endpoint="/users", data=user_data)