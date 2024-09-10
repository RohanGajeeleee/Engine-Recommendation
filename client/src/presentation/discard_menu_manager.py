import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.RequestBuilder import FeedbackRequestBuilder
from src.common.RequestBuilder import DiscardMenuRequestBuilder
from src.common.input_validation import InputValidator

class DiscardMenuManager:
    def __init__(self):
        self.input_validator = InputValidator()

    def show_discard_menu(self):
        from src.presentation.discard_menu import DiscardMenu
        discard_menu = DiscardMenu()
        discard_menu.display()

    def view_discarded_items(self):
        request =  DiscardMenuRequestBuilder.view_discarded_items_request()
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error viewing discarded items: {e}")
            print("An error occurred while fetching discarded items.")
        return True

    def restore_item(self):
        item_id = self.input_validator.get_valid_item_id("Enter item ID to restore: ")
        request = DiscardMenuRequestBuilder.restore_discarded_item_request(item_id)
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error restoring item {item_id}: {e}")
            print(f"An error occurred while restoring item ID {item_id}.")
        return True

    def delete_item(self):
        item_id = self.input_validator.get_valid_item_id("Enter item ID to delete permanently: ")
        request = DiscardMenuRequestBuilder.delete_discarded_item_request(item_id)
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error deleting item {item_id}: {e}")
            print(f"An error occurred while deleting item ID {item_id}.")
        return True

    def request_feedback(self):
        item_id = self.input_validator.get_valid_item_id("Enter item ID to request feedback on: ")
        request = FeedbackRequestBuilder.request_feedback_on_discarded_item_request(item_id)
        try:
            response = send_request(request)
            print(response)
        except Exception as e:
            logging.error(f"Error requesting feedback for item {item_id}: {e}")
            print(f"An error occurred while requesting feedback for item ID {item_id}.")
        return True

    def view_feedback_replies(self):
        request = FeedbackRequestBuilder.view_feedback_replies_request()
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
