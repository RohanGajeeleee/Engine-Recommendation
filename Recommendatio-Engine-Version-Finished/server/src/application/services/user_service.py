import logging
from src.infrastructure.repositories.user_repository import UserRepository
from src.domain.models.user import User
from src.application.services.profile_service import ProfileService

logging.basicConfig(level=logging.INFO)

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.profile_service = ProfileService()

    def register_user(self, employee_id, name, password, role, dietary_preference=None, spice_level=None, cuisine_preference=None, sweet_tooth=None):
        try:
            user = User(employee_id=employee_id, name=name, password=password, role=role)
            self.user_repository.save(user)
            logging.info(f"Registered user: {employee_id}")
            
            if role == 'employee':
                profile_response = self.profile_service.create_profile(employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
                if profile_response != "Profile created successfully":
                    logging.error(f"Failed to create profile for employee: {employee_id}")
                    return f"User registered but failed to create profile: {profile_response}"
            
            return "User registered successfully"
        except Exception as e:
            logging.error(f"Error registering user: {e}")
            return f"Error registering user: {e}"

    def authenticate_user(self, employee_id, password):
        try:
            user = self.user_repository.find_by_id(employee_id)
            if user and user.check_password(password):
                logging.info(f"Authenticated user: {employee_id}")
                return user.role
            else:
                logging.warning(f"Authentication failed for user: {employee_id}")
                return None
        except Exception as e:
            logging.error(f"Error authenticating user: {e}")
            return None
