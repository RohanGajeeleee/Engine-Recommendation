import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.input_validation import InputValidator

class ProfileManager:
    def __init__(self):
        self.input_validator = InputValidator()

    def update_profile(self, employee_id):
        dietary_preference = self.input_validator.get_valid_dietary_type("Enter dietary preference (1 for Vegetarian, 2 for Non-Vegetarian, 3 for Eggetarian): ", allow_empty=False)
        spice_level = self.input_validator.get_valid_spice_level("Enter spice level (1 for Low, 2 for Medium, 3 for High): ", allow_empty=False)
        cuisine_preference = self.input_validator.get_valid_food_category("Enter cuisine preference (1 for North Indian, 2 for South Indian, 3 for Other): ", allow_empty=False)
        sweet_tooth = self.input_validator.get_valid_sweet_tooth("Do you have a sweet tooth? (1 for Yes, 2 for No): ", allow_empty=False)

        request = f"UPDATE_PROFILE {employee_id} {dietary_preference} {spice_level} {cuisine_preference} {sweet_tooth}"
        response = send_request(request)
        print(response)
        return True
