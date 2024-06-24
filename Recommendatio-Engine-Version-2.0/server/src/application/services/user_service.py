import sys
import os

# Adjust the path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.domain.models.user import User
from src.infrastructure.user_repository import UserRepository

class UserService:
    @staticmethod
    def handle_request(request):
        parts = request.split()
        command = parts[0]
        
        if command == "AUTH":
            employee_id, password = parts[1], parts[2]
            return UserService.authenticate(employee_id, password)
        elif command == "REGISTER":
            employee_id, name, password, role = parts[1], parts[2], parts[3], parts[4]
            return UserService.register(employee_id, name, password, role)
        return "INVALID REQUEST"

    @staticmethod
    def authenticate(employee_id, password):
        user_repo = UserRepository()
        user = user_repo.find_by_id(employee_id)
        if user and user.check_password(password):
            return f"Authenticated as {user.role}"
        return "Authentication failed"

    @staticmethod
    def register(employee_id, name, password, role):
        user = User(employee_id, name, User.hash_password(password), role)
        user_repo = UserRepository()
        if user_repo.save(user):
            return "Registration successful"
        return "Registration failed"
