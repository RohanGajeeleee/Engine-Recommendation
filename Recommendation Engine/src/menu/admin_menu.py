import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.menu_service import MenuService

class AdminMenu:
    MENU_CHOICES = {
        'ADD_ITEM': '1',
        'UPDATE_ITEM': '2',
        'DELETE_ITEM': '3',
        'LOGOUT': '4'
    }

    @staticmethod
    def display():
        print("\nAdmin Menu")
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. Logout")

    @staticmethod
    def handle_choice(choice):
        actions = {
            AdminMenu.MENU_CHOICES['ADD_ITEM']: MenuService.add_item,
            AdminMenu.MENU_CHOICES['UPDATE_ITEM']: MenuService.update_item,
            AdminMenu.MENU_CHOICES['DELETE_ITEM']: MenuService.delete_item,
            AdminMenu.MENU_CHOICES['LOGOUT']: AdminMenu.logout
        }

        action = actions.get(choice, AdminMenu.invalid_choice)
        return action()

    @staticmethod
    def logout():
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True
