
from common.input_validation import InputValidator
import logging
class MenuValidator:
    @staticmethod
    def get_existing_item_id(prompt, fetcher_method):
        item_details = fetcher_method()
        item_ids = [item['id'] for item in item_details]
        while True:
            item_id = InputValidator.get_valid_item_id(prompt)
            if item_id in item_ids:
                return item_id
            else:
                print(f"Item ID {item_id} does not exist. Please enter a valid item ID.")

    @staticmethod
    def get_existing_choice_id(user_choices, prompt):
        item_ids = [choice['menu_id'] for choice in user_choices]
        while True:
            item_id = InputValidator.get_valid_item_id(prompt)
            if item_id in item_ids:
                return item_id
            else:
                print(f"Item ID {item_id} is not in your chosen items. Please enter a valid item ID.")
                
    @staticmethod
    def get_existing_current_item_id(prompt, fetcher_method):
        item_details = fetcher_method()
        item_ids = [item['id'] for item in item_details]
        while True:
            item_id = InputValidator.get_valid_item_id(prompt)
            if item_id in item_ids:
                return item_id
            else:
                logging.warning(f"Item ID {item_id} does not exist in the current menu.")
                print(f"Item ID {item_id} does not exist in the current menu. Please enter a valid item ID.")
