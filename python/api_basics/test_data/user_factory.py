from .user import User
from .user_data import USER_DATA

class UserFactory:

    def create_user_data(self, first_name = USER_DATA["first_name"], last_name = USER_DATA["last_name"], phone=USER_DATA["phone"], email=USER_DATA["email"], address=USER_DATA["address"], status = 'new', gender = None):
        return User(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address, status=status, gender=gender)

