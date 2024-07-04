import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.input_validation import InputValidator
from src.presentation.discard_menu_manager import DiscardMenuManager

class DiscardMenu:
    MENU_CHOICES = {
        'VIEW_DISCARDED_ITEMS': '1',
        'RESTORE_ITEM': '2',
        'DELETE_ITEM': '3',
        'REQUEST_FEEDBACK': '4',
        'VIEW_FEEDBACK_REPLIES': '5',
        'BACK': '6'
    }

    def __init__(self):
        self.input_validator = InputValidator()
        self.discard_menu_manager = DiscardMenuManager()

    def display(self):
        while True:
            print("\nDiscard Menu")
            print("1. View Discarded Items")
            print("2. Restore Item to Menu")
            print("3. Delete Item Permanently")
            print("4. Request Feedback on Discarded Item")
            print("5. View Feedback Replies")
            print("6. Back to Chef Menu")

            choice = self.input_validator.get_valid_input("Enter choice: ")
            if not self.handle_choice(choice):
                break

    def handle_choice(self, choice):
        actions = {
            self.MENU_CHOICES['VIEW_DISCARDED_ITEMS']: self.discard_menu_manager.view_discarded_items,
            self.MENU_CHOICES['RESTORE_ITEM']: self.discard_menu_manager.restore_item,
            self.MENU_CHOICES['DELETE_ITEM']: self.discard_menu_manager.delete_item,
            self.MENU_CHOICES['REQUEST_FEEDBACK']: self.discard_menu_manager.request_feedback,
            self.MENU_CHOICES['VIEW_FEEDBACK_REPLIES']: self.discard_menu_manager.view_feedback_replies,
            self.MENU_CHOICES['BACK']: self.back_to_chef_menu
        }
        action = actions.get(choice, self.invalid_choice)
        return action()

    def back_to_chef_menu(self):
        return False

    def invalid_choice(self):
        print("Invalid choice. Please try again.")
        return True
