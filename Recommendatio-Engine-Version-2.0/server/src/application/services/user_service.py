# server/src/application/services/user_service.py

import logging
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.models.user import User

logging.basicConfig(level=logging.INFO)

class UserService:
    @staticmethod
    def register_user(employee_id, name, password, role):
        try:
            user = User(employee_id=employee_id, name=name, password=password, role=role)
            UserRepository.save(user)
            logging.info(f"Registered user: {employee_id}")
            return "User registered successfully"
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return f"Error registering user: {e}"

    @staticmethod
    def authenticate_user(employee_id, password):
        try:
            user = UserRepository.find_by_id(employee_id)
            if user and user.check_password(password):
                logging.info(f"Authenticated user: {employee_id}")
                return user.role
            else:
                logging.warning(f"Authentication failed for user: {employee_id}")
                return None
        except Exception as e:
            logging.error(f"Error authenticating user: {e}")
            return None
