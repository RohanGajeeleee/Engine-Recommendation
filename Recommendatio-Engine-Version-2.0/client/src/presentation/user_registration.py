import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.input_validation import InputValidator

class UserRegistration:
    def __init__(self):
        self.input_validator = InputValidator()

    def register(self):
        try:
            employee_id = self.input_validator.get_valid_item_id("Enter employee ID: ")
            name = self.input_validator.get_valid_input("Enter name: ")
            password = self.input_validator.get_valid_input("Enter password: ")
            role = self.input_validator.get_valid_role("Enter role (admin, chef, employee): ")

            if role == 'employee':
                dietary_preference = self.input_validator.get_valid_dietary_type("Enter dietary preference (1 for Vegetarian, 2 for Non-Vegetarian, 3 for Eggetarian): ")
                spice_level = self.input_validator.get_valid_spice_level("Enter spice level (1 for Low, 2 for Medium, 3 for High): ")
                cuisine_preference = self.input_validator.get_valid_food_category("Enter cuisine preference (1 for North Indian, 2 for South Indian, 3 for Other): ")
                sweet_tooth = self.input_validator.get_valid_sweet_tooth("Do you have a sweet tooth? (1 for Yes, 2 for No): ")

                profile_details = f"{dietary_preference} {spice_level} {cuisine_preference} {sweet_tooth}"
            else:
                profile_details = ""

            request = f"REGISTER {employee_id} {name} {password} {role} {profile_details}"
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error during registration: {e}")
            print("An error occurred during registration. Please try again.")
