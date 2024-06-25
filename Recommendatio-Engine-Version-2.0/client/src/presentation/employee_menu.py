# client/src/presentation/employee_menu.py

import sys
import os

# Adjust the path to include the root directory and common directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common.network_utils import send_request
from common.input_validation import InputValidator
from common.menu_item_checker import MenuItemChecker

class EmployeeMenu:
    MENU_CHOICES = {
        'ADD_FEEDBACK': '1',
        'VIEW_FEEDBACK': '2',
        'CHOOSE_RECOMMENDED_ITEM': '3',
        'VIEW_NOTIFICATIONS': '4',
        'LOGOUT': '5'
    }

    @staticmethod
    def display():
        print("\nEmployee Menu")
        print("1. Add Feedback")
        print("2. View Feedback")
        print("3. Choose Recommended Item")
        print("4. View Notifications")
        print("5. Logout")

    @staticmethod
    def handle_choice(employee_id, choice, first_day, current_date):
        actions = {
            EmployeeMenu.MENU_CHOICES['ADD_FEEDBACK']: lambda: EmployeeMenu.add_feedback(employee_id, current_date),
            EmployeeMenu.MENU_CHOICES['VIEW_FEEDBACK']: EmployeeMenu.view_feedback,
            EmployeeMenu.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']: lambda: EmployeeMenu.choose_recommended_item(employee_id),
            EmployeeMenu.MENU_CHOICES['VIEW_NOTIFICATIONS']: lambda: EmployeeMenu.view_notifications(employee_id),
            EmployeeMenu.MENU_CHOICES['LOGOUT']: EmployeeMenu.logout
        }
        action = actions.get(choice, EmployeeMenu.invalid_choice)
        return action()

    @staticmethod
    def add_feedback(employee_id, current_date):
        time_of_day = InputValidator.get_valid_time_of_day("Enter time of day (breakfast, lunch, dinner): ")
        user_choices = MenuItemChecker.fetch_user_choices(employee_id, time_of_day)
        if not user_choices:
            print("No menu items available to give feedback.")
            return True

        print("\nYour Chosen Menu Items:")
        for choice in user_choices:
            print(f"ID: {choice['menu_id']}, Name: {choice['name']}")

        item_id = MenuItemChecker.get_existing_choice_id(user_choices, "Enter item ID to give feedback on: ")
        rating = InputValidator.get_valid_rating("Enter your rating (1-5): ")
        comment = InputValidator.get_valid_input("Enter your feedback: ")

        request = f"ADD_FEEDBACK {employee_id} {item_id} {rating} {comment} {time_of_day} {current_date}"
        response = send_request(request)
        print(response)
        return True
    @staticmethod
    def view_feedback():
        request = "VIEW_FEEDBACK"
        response = send_request(request)
        print(response)
        return True

    @staticmethod
    def choose_recommended_item(employee_id):
        # Fetch the current menu items
        current_menu_items = MenuItemChecker.fetch_current_menu_items()

        # Display current menu items
        print("\nCurrent Menu Items:")
        for item in current_menu_items:
            print(f"ID: {item['id']}, Name: {item['name']}")

        item_id = MenuItemChecker.get_existing_current_item_id("Enter item ID to choose: ")
        time_of_day = InputValidator.get_valid_time_of_day("Enter time of day (breakfast, lunch, dinner): ")
        request = f"CHOOSE_RECOMMENDED_ITEM {employee_id} {item_id} {time_of_day}"
        response = send_request(request)
        print(response)
        return True

    @staticmethod
    def view_notifications(employee_id):
        request = f"VIEW_NOTIFICATIONS {employee_id}"
        response = send_request(request)
        print(response)
        return True

    @staticmethod
    def logout():
        print("Logged out successfully")
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True