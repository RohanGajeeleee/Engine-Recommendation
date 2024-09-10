import hashlib

class User:
    def __init__(self, employee_id, name, password, role):
        self.employee_id = employee_id
        self.name = name
        self.password = password
        self.role = role

    def check_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
