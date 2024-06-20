import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.menu_service import MenuService
from src.models.user import User

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
    def handle_choice(choice, employee_id):
        actions = {
            AdminMenu.MENU_CHOICES['ADD_ITEM']: lambda: AdminMenu.add_item(employee_id),
            AdminMenu.MENU_CHOICES['UPDATE_ITEM']: lambda: AdminMenu.update_item(employee_id),
            AdminMenu.MENU_CHOICES['DELETE_ITEM']: lambda: AdminMenu.delete_item(employee_id),
            AdminMenu.MENU_CHOICES['VIEW_MENU']: lambda: AdminMenu.view_menu(employee_id),
            AdminMenu.MENU_CHOICES['LOGOUT']: lambda: AdminMenu.logout(employee_id)
        }

        action = actions.get(choice, lambda: AdminMenu.invalid_choice(employee_id))
        return action()

    @staticmethod
    def add_item(employee_id):
        MenuService.add_item()
        User.log_activity(employee_id, 'add_item', 'Added menu item')
        return True

    @staticmethod
    def update_item(employee_id):
        MenuService.update_item()
        User.log_activity(employee_id, 'update_item', 'Updated menu item')
        return True

    @staticmethod
    def delete_item(employee_id):
        MenuService.delete_item()
        User.log_activity(employee_id, 'delete_item', 'Deleted menu item')
        return True

    @staticmethod
    def view_menu(employee_id):
        MenuService.list_items()
        User.log_activity(employee_id, 'view_menu', 'Viewed all menu items')
        return True

    @staticmethod
    def logout(employee_id):
        User.log_activity(employee_id, 'logout', 'User logged out')
        return False

    @staticmethod
    def invalid_choice(employee_id):
        print("Invalid choice. Please try again.")
        User.log_activity(employee_id, 'invalid_choice', 'Invalid menu choice')
        return True
