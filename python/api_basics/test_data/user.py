class User:
    def __init__(self,first_name, last_name, phone, email, address, status = 'new', gender = None):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone = phone
        self.email = email
        self.address = address
        self.status = status

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone} {self.email} {self.address} {self.status} {self.gender}"

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "status": self.status,
        }

user1 = User("Ilya", "Petrov", "9061221212", "test@test.test","Yaroslavl","success", "male")
print(user1)