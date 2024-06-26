import sys
import os

# Adjust the path to include the root directory and common directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common.network_utils import send_request
from common.menu_item_checker import MenuItemChecker
from common.input_validation import InputValidator

class ChefMenu:
    MENU_CHOICES = {
        'VIEW_FEEDBACK': '1',
        'CHOOSE_MENU_ITEMS': '2',
        'GENERATE_RECOMMENDATIONS': '3',
        'LOGOUT': '4'
    }

    @staticmethod
    def display():
        print("\nChef Menu")
        print("1. View Feedback")
        print("2. Choose Menu Items")
        print("3. Generate Recommendations")
        print("4. Logout")

    @staticmethod
    def handle_choice(chef_id, choice):
        actions = {
            ChefMenu.MENU_CHOICES['VIEW_FEEDBACK']: FeedbackManager.view_feedback,
            ChefMenu.MENU_CHOICES['CHOOSE_MENU_ITEMS']: MenuManager.choose_menu_items,
            ChefMenu.MENU_CHOICES['GENERATE_RECOMMENDATIONS']: RecommendationManager.generate_recommendations,
            ChefMenu.MENU_CHOICES['LOGOUT']: ChefMenu.logout
        }
        action = actions.get(choice, ChefMenu.invalid_choice)
        return action(chef_id)

    @staticmethod
    def logout(chef_id):
        print("Logged out successfully")
        return False

    @staticmethod
    def invalid_choice(chef_id):
        print("Invalid choice. Please try again.")
        return True

class FeedbackManager:
    @staticmethod
    def view_feedback(chef_id):
        request = "VIEW_FEEDBACK"
        response = send_request(request)
        print(response)
        return True

class MenuManager:
    @staticmethod
    def choose_menu_items(chef_id):
        clear_request = "CLEAR_CURRENT_MENU"
        clear_response = send_request(clear_request)
        if clear_response != "Current menu cleared":
            print("Error clearing current menu.")
            return True

        print("Current menu cleared. Please choose new items.")
        items_added = False
        view_request = "VIEW_MENU"
        view_response = send_request(view_request)
        print(view_response)
        
        available_items = MenuItemChecker.parse_available_items(view_response)

        while True:
            item_id = input("Enter item ID to add to current menu or 'done' to finish: ")
            if item_id.lower() == 'done':
                if items_added:
                    break
                else:
                    print("You must add at least one item to the current menu before finishing.")
                    continue
            if not item_id.isdigit() or not MenuItemChecker.is_item_available(int(item_id), available_items):
                print(f"Item ID {item_id} is unavailable. Please choose an available item.")
                continue

            add_request = f"ADD_TO_CURRENT_MENU {item_id}"
            add_response = send_request(add_request)
            if "successfully" in add_response:
                items_added = True
            print(add_response)

        return True

class RecommendationManager:
    @staticmethod
    def generate_recommendations(chef_id):
        try:
            num_recommendations = int(input("Enter the number of recommendations you want to generate: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return True

        request = f"GENERATE_RECOMMENDATIONS {num_recommendations}"
        response = send_request(request)
        print(response)

        fetch_request = f"FETCH_RECOMMENDATIONS {num_recommendations}"
        fetch_response = send_request(fetch_request)
        print(fetch_response)

        return True
