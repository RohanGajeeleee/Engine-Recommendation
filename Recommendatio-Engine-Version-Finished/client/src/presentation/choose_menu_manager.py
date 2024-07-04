import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.network_utils import send_request
from src.common.menu_item_checker import MenuItemChecker

class ChooseMenuManager:
    def __init__(self):
        self.menu_item_checker = MenuItemChecker()

    def choose_menu_items(self):
        send_request("CHECK_DISCARDED_ITEMS")
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
        
        available_items = self.menu_item_checker.parse_available_items(view_response)

        while True:
            item_id = input("Enter item ID to add to current menu or 'done' to finish: ").strip()
            if item_id.lower() == 'done':
                if items_added:
                    finalize_request = "FINALIZE_CURRENT_MENU"
                    finalize_response = send_request(finalize_request)
                    print(finalize_response)
                    break
                else:
                    print("You must add at least one item to the current menu before finishing.")
                    continue
            if not item_id:
                print("Input cannot be empty. Please enter a valid item ID.")
                continue
            if not item_id.isdigit():
                print(f"Invalid input '{item_id}'. Please enter a valid item ID.")
                continue
            try:
                item_id = int(item_id)
            except ValueError as e:
                logging.error(f"Error converting item ID to int: {e}")
                print(f"Invalid input '{item_id}'. Please enter a valid item ID.")
                continue

            if not self.menu_item_checker.is_item_available(available_items, item_id):
                print(f"Item ID {item_id} is unavailable. Please choose an available item.")
                continue

            add_request = f"ADD_TO_CURRENT_MENU {item_id}"
            add_response = send_request(add_request)
            if "successfully" in add_response:
                items_added = True
            print(add_response)

        return True
