import sys
import os

# Adjust the path to include the root directory and common directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common.network_utils import send_request
from common.input_validation import InputValidator
from common.menu_item_checker import MenuItemChecker
import logging
class EmployeeMenu:
    MENU_CHOICES = {
        'ADD_FEEDBACK': '1',
        'VIEW_FEEDBACK': '2',
        'CHOOSE_RECOMMENDED_ITEM': '3',
        'VIEW_NOTIFICATIONS': '4',
        'REPLY_FEEDBACK_REQUEST': '5',
        'UPDATE_PROFILE': '6',
        'LOGOUT': '7'
    }

    @staticmethod
    def display():
        print("\nEmployee Menu")
        print("1. Add Feedback")
        print("2. View Feedback")
        print("3. Choose Recommended Item")
        print("4. View Notifications")
        print("5. Reply to Feedback Request")
        print("6. Update Profile")
        print("7. Logout")
    

    @staticmethod
    def handle_choice(employee_id, choice, first_day, current_date):
        actions = {
            EmployeeMenu.MENU_CHOICES['ADD_FEEDBACK']: lambda: FeedbackManager.add_feedback(employee_id, current_date),
            EmployeeMenu.MENU_CHOICES['VIEW_FEEDBACK']: FeedbackManager.view_feedback,
            EmployeeMenu.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']: lambda: RecommendationManager.choose_recommended_item(employee_id),
            EmployeeMenu.MENU_CHOICES['VIEW_NOTIFICATIONS']: lambda: NotificationManager.view_notifications(employee_id),
            EmployeeMenu.MENU_CHOICES['REPLY_FEEDBACK_REQUEST']: lambda: FeedbackRequestManager.reply_to_request(employee_id),
            EmployeeMenu.MENU_CHOICES['UPDATE_PROFILE']: lambda: ProfileManager.update_profile(employee_id),
            EmployeeMenu.MENU_CHOICES['LOGOUT']: UserSession.logout
        }
        action = actions.get(choice, UserSession.invalid_choice)
        return action()
class ProfileManager:
    @staticmethod
    def update_profile(employee_id):
        dietary_preference = InputValidator.get_valid_dietary_type("Enter dietary preference (1 for Vegetarian, 2 for Non-Vegetarian, 3 for Eggetarian): ", allow_empty=True)
        spice_level = InputValidator.get_valid_spice_level("Enter spice level (1 for Low, 2 for Medium, 3 for High): ", allow_empty=True)
        cuisine_preference = InputValidator.get_valid_food_category("Enter cuisine preference (1 for North Indian, 2 for South Indian, 3 for Other): ", allow_empty=True)
        sweet_tooth = InputValidator.get_valid_sweet_tooth("Do you have a sweet tooth? (1 for Yes, 2 for No): ", allow_empty=True)

        request = f"UPDATE_PROFILE {employee_id} {dietary_preference} {spice_level} {cuisine_preference} {sweet_tooth}"
        response = send_request(request)
        print(response)
        return True
class FeedbackManager:
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

class RecommendationManager:
    @staticmethod
    def choose_recommended_item(employee_id):
        request = f"FETCH_SORTED_MENU {employee_id}"
        response = send_request(request)
        
        if response.startswith("No preferences found") or response.startswith("Error"):
            print(response)
            return False
        
        print(response)

        item_id = MenuItemChecker.get_existing_current_item_id("Enter item ID to choose: ")
        time_of_day = InputValidator.get_valid_time_of_day("Enter time of day (breakfast, lunch, dinner): ")
        request = f"CHOOSE_RECOMMENDED_ITEM {employee_id} {item_id} {time_of_day}"
        response = send_request(request)
        print(response)
        return True

class NotificationManager:
    @staticmethod
    def view_notifications(employee_id):
        request = f"VIEW_NOTIFICATIONS {employee_id}"
        response = send_request(request)
        print(response)
        return True

class FeedbackRequestManager:
    @staticmethod
    def reply_to_request(employee_id):
        request = f"FETCH_FEEDBACK_REQUESTS {employee_id}"
        response = send_request(request)
        feedback_requests = response.split('\n')
        
        feedback_requests = [req for req in feedback_requests if "ID:" in req]
        
        if not feedback_requests or feedback_requests[0].strip() == "":
            print("No feedback requests available.")
            return True

        print("\nFeedback Requests:")
        for i, request in enumerate(feedback_requests, start=1):
            print(f"{i}. {request}")

        choice = InputValidator.get_valid_number("Select the request you want to reply to (number): ")
        if choice < 1 or choice > len(feedback_requests):
            print("Invalid choice.")
            return True

        selected_request = feedback_requests[choice - 1]

        if "ID: " not in selected_request:
            print("Invalid request format.")
            return True

        try:
            request_id = int(selected_request.split("ID: ")[1].split(",")[0])
            menu_id = int(selected_request.split("MenuID: ")[1].split(")")[0])
        except (IndexError, ValueError) as e:
            print(f"Error parsing request ID or menu ID: {e}")
            return True

        q1 = InputValidator.get_valid_input("What didn’t you like about this item? ")
        q2 = InputValidator.get_valid_input("How would you like this item to taste? ")
        q3 = InputValidator.get_valid_input("Share your mom’s recipe for this item. ")

        feedback_reply = f"REPLY_FEEDBACK_REQUEST {employee_id} {request_id} {menu_id} {q1} {q2} {q3}"
        response = send_request(feedback_reply)
        print(response)
        return True

class UserSession:
    @staticmethod
    def logout():
        print("Logged out successfully")
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True
