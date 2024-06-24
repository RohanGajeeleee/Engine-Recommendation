import hashlib

class User:
    def __init__(self, employee_id, name=None, password=None, role=None):
        self.employee_id = employee_id
        self.name = name
        self.password = password
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()
