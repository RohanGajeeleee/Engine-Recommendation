import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.input_validation import InputValidator
from src.common.menu_item_checker import MenuItemChecker

class FeedbackManager:
    def __init__(self):
        self.input_validator = InputValidator()
        self.menu_item_checker = MenuItemChecker()

    def add_feedback(self, employee_id, current_date):
        time_of_day = self.input_validator.get_valid_time_of_day("Enter time of day (breakfast, lunch, dinner): ")
        user_choices = self.menu_item_checker.fetch_user_choices(employee_id, time_of_day)
        if not user_choices:
            print("No menu items available to give feedback.")
            return True

        print("\nYour Chosen Menu Items:")
        for choice in user_choices:
            print(f"ID: {choice['menu_id']}, Name: {choice['name']}")

        item_id = self.menu_item_checker.get_existing_choice_id(user_choices, "Enter item ID to give feedback on: ")
        rating = self.input_validator.get_valid_rating("Enter your rating (1-5): ")
        comment = self.input_validator.get_valid_input("Enter your feedback: ")

        request = f"ADD_FEEDBACK {employee_id} {item_id} {rating} {comment} {time_of_day} {current_date}"
        response = send_request(request)
        print(response)
        return True

    def view_feedback(self):
        request = "VIEW_FEEDBACK"
        response = send_request(request)
        print(response)
        return True
