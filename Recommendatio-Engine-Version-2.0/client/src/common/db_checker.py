# client/src/common/db_checker.py

from common.network_utils import send_request
from common.input_validation import InputValidator

class DBChecker:
    @staticmethod
    def fetch_item_ids():
        request = "VIEW_MENU"
        response = send_request(request)
        items = response.split('\n')
        item_ids = []
        for item in items:
            if item.startswith("ID:"):
                item_id = int(item.split(',')[0].split(':')[1].strip())
                item_ids.append(item_id)
        return item_ids

    @staticmethod
    def get_existing_item_id(prompt):
        item_ids = DBChecker.fetch_item_ids()
        while True:
            item_id = InputValidator.get_valid_item_id(prompt)
            if item_id in item_ids:
                return item_id
            else:
                print(f"Item ID {item_id} does not exist. Please enter a valid item ID.")
