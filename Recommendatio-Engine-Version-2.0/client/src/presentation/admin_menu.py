
import sys
import os

# Adjust the path to include the root directory and common directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common.network_utils import send_request
from common.input_validation import InputValidator
from src.common.menu_item_checker import MenuItemChecker

class AdminMenu:
    MENU_CHOICES = {
        'ADD_ITEM': '1',
        'UPDATE_ITEM': '2',
        'DELETE_ITEM': '3',
        'VIEW_MENU': '4',
        'LOGOUT': '5'
    }

    @staticmethod
    def display():
        print("\nAdmin Menu")
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. View All Menu Items")
        print("5. Logout")

    @staticmethod
    def handle_choice(choice):
        actions = {
            AdminMenu.MENU_CHOICES['ADD_ITEM']: AdminMenu.add_item,
            AdminMenu.MENU_CHOICES['UPDATE_ITEM']: AdminMenu.update_item,
            AdminMenu.MENU_CHOICES['DELETE_ITEM']: AdminMenu.delete_item,
            AdminMenu.MENU_CHOICES['VIEW_MENU']: AdminMenu.view_menu,
            AdminMenu.MENU_CHOICES['LOGOUT']: AdminMenu.logout
        }
        action = actions.get(choice, AdminMenu.invalid_choice)
        return action()

    @staticmethod
    def add_item():
        name = InputValidator.get_valid_input("Enter item name: ")
        price = InputValidator.get_valid_price("Enter item price: ")
        availability = InputValidator.get_valid_availability("Enter availability (1 for Available, 2 for Unavailable): ")
        request = f"ADD_ITEM {name} {price} {availability}"
        response = send_request(request)
        print(response)
        return True

    @staticmethod
    def update_item():
        AdminMenu.view_menu()
        item_id = MenuItemChecker.get_existing_item_id("Enter item ID to update: ")
        name = InputValidator.get_valid_input("Enter new name (or leave blank to keep current): ", allow_empty=True)
        price = InputValidator.get_valid_price("Enter new price (or leave blank to keep current): ", allow_empty=True)
        availability = InputValidator.get_valid_availability("Enter new availability (1 for Available, 2 for Unavailable, or leave blank to keep current): ", allow_empty=True)
        request = f"UPDATE_ITEM {item_id} {name if name else 'null'} {price if price else 'null'} {availability if availability else 'null'}"
        response = send_request(request)
        print(response)
        return True

    @staticmethod
    def delete_item():
        AdminMenu.view_menu()
        item_id = MenuItemChecker.get_existing_item_id("Enter item ID to delete: ")
        request = f"DELETE_ITEM {item_id}"
        response = send_request(request)
        print(response)
        return True

    @staticmethod
    def view_menu():
        request = "VIEW_MENU"
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
