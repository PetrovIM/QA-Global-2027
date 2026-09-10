from .user import User

class UserFactory:

    def create_user_data(self, first_name, last_name, phone, email, address, status = 'new', gender = None):
        return User(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address, status=status, gender=gender)