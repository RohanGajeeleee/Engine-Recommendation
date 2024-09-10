import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.presentation.menu_manager import MenuManager

class AdminMenu:
    MENU_CHOICES = {
        'ADD_ITEM': '1',
        'UPDATE_ITEM': '2',
        'DELETE_ITEM': '3',
        'VIEW_MENU': '4',
        'LOGOUT': '5'
    }

    def __init__(self):
        self.menu_manager = MenuManager()

    def display(self):
        print("\nAdmin Menu")
        print("1. Add Menu Item")
        print("2. Update Menu Item")
        print("3. Delete Menu Item")
        print("4. View All Menu Items")
        print("5. Logout")

    def handle_choice(self, choice):
        actions = {
            AdminMenu.MENU_CHOICES['ADD_ITEM']: self.menu_manager.add_item,
            AdminMenu.MENU_CHOICES['UPDATE_ITEM']: self.menu_manager.update_item,
            AdminMenu.MENU_CHOICES['DELETE_ITEM']: self.menu_manager.delete_item,
            AdminMenu.MENU_CHOICES['VIEW_MENU']: self.menu_manager.view_menu,
            AdminMenu.MENU_CHOICES['LOGOUT']: self.logout
        }
        action = actions.get(choice, self.invalid_choice)
        return action()

    def logout(self):
        print("Logged out successfully")
        return False

    def invalid_choice(self):
        print("Invalid choice. Please try again.")
        return True
