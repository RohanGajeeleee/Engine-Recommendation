import logging
from src.infrastructure.repositories.Profile_repository import ProfileRepository

class ProfileService:
    def __init__(self):
        self.profile_repository = ProfileRepository()

    def update_profile(self, employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth):
        try:
            profile = {
                'employee_id': employee_id,
                'dietary_preference': dietary_preference,
                'spice_level': spice_level,
                'cuisine_preference': cuisine_preference,
                'sweet_tooth': sweet_tooth
            }
            self.profile_repository.update(profile)
            logging.info(f"Updated profile for employee ID: {employee_id}")
            return "Profile updated successfully"
        except Exception as e:
            logging.error(f"Error updating profile: {e}")
            return f"Error updating profile: {e}"

    def create_profile(self, employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth):
        try:
            profile = {
                'employee_id': employee_id,
                'dietary_preference': dietary_preference,
                'spice_level': spice_level,
                'cuisine_preference': cuisine_preference,
                'sweet_tooth': sweet_tooth
            }
            self.profile_repository.create_profile(profile)
            logging.info(f"Created profile for employee ID: {employee_id}")
            return "Profile created successfully"
        except Exception as e:
            logging.error(f"Error creating profile: {e}")
            return f"Error creating profile: {e}"

    def get_user_preferences(self, employee_id):
        try:
            profile = self.profile_repository.get_profile(employee_id)
            if profile:
                return {
                    'spice_level': profile['spice_level'],
                    'cuisine_preference': profile['cuisine_preference'],  
                    'sweet_tooth': profile['sweet_tooth'],
                    'dietary_preference': profile['dietary_preference']
                }
            else:
                logging.error(f"No profile found for employee ID: {employee_id}")
                return None
        except Exception as e:
            logging.error(f"Error fetching profile for employee ID: {employee_id}: {e}")
            return None