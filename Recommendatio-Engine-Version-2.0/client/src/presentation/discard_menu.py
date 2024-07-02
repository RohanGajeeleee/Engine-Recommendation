import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from common.network_utils import send_request
from common.input_validation import InputValidator
from src.presentation.chef_menu import ChefMenu

class DiscardMenu:
    MENU_CHOICES = {
        'VIEW_DISCARDED_ITEMS': '1',
        'RESTORE_ITEM': '2',
        'DELETE_ITEM': '3',
        'REQUEST_FEEDBACK': '4',
        'VIEW_FEEDBACK_REPLIES': '5',
        'BACK': '6'
    }

    @staticmethod
    def display():
        while True:
            print("\nDiscard Menu")
            print("1. View Discarded Items")
            print("2. Restore Item to Menu")
            print("3. Delete Item Permanently")
            print("4. Request Feedback on Discarded Item")
            print("5. View Feedback Replies")
            print("6. Back to Chef Menu")

            choice = InputValidator.get_valid_input("Enter choice: ")
            if not DiscardMenu.handle_choice(choice):
                break

    @staticmethod
    def handle_choice(choice):
        actions = {
            DiscardMenu.MENU_CHOICES['VIEW_DISCARDED_ITEMS']: DiscardActions.view_discarded_items,
            DiscardMenu.MENU_CHOICES['RESTORE_ITEM']: DiscardActions.restore_item,
            DiscardMenu.MENU_CHOICES['DELETE_ITEM']: DiscardActions.delete_item,
            DiscardMenu.MENU_CHOICES['REQUEST_FEEDBACK']: DiscardActions.request_feedback,
            DiscardMenu.MENU_CHOICES['VIEW_FEEDBACK_REPLIES']: DiscardActions.view_feedback_replies,
            DiscardMenu.MENU_CHOICES['BACK']: DiscardMenu.back_to_chef_menu
        }
        action = actions.get(choice, DiscardMenu.invalid_choice)
        return action()

    @staticmethod
    def back_to_chef_menu():
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True

class DiscardActions:
    @staticmethod
    def view_discarded_items():
        request = "VIEW_DISCARDED_ITEMS"
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error viewing discarded items: {e}")
            print("An error occurred while fetching discarded items.")
        return True

    @staticmethod
    def restore_item():
        item_id = InputValidator.get_valid_item_id("Enter item ID to restore: ")
        request = f"RESTORE_DISCARDED_ITEM {item_id}"
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error restoring item {item_id}: {e}")
            print(f"An error occurred while restoring item ID {item_id}.")
        return True

    @staticmethod
    def delete_item():
        item_id = InputValidator.get_valid_item_id("Enter item ID to delete permanently: ")
        request = f"DELETE_DISCARDED_ITEM {item_id}"
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error deleting item {item_id}: {e}")
            print(f"An error occurred while deleting item ID {item_id}.")
        return True

    @staticmethod
    def request_feedback():
        item_id = InputValidator.get_valid_item_id("Enter item ID to request feedback on: ")
        request = f"REQUEST_FEEDBACK_ON_DISCARDED_ITEM {item_id}"
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error requesting feedback for item {item_id}: {e}")
            print(f"An error occurred while requesting feedback for item ID {item_id}.")
        return True

    @staticmethod
    def view_feedback_replies():
        request = "VIEW_FEEDBACK_REPLIES"
        try:
            response = send_request(request)
            replies = response.strip().split('\n')
            if len(replies) <= 1: 
                print("No feedback replies available.")
                return True

            print("\nFeedback Replies:")
            for reply in replies[1:]: 
                print(reply)
        except Exception as e:
            logging.error(f"Error viewing feedback replies: {e}")
            print("An error occurred while fetching feedback replies.")
        return True
