import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from common.network_utils import send_request

class MenuFetcher:
    def __init__(self):
        pass

    def fetch_item_ids(self):
        try:
            request = "VIEW_MENU"
            response = send_request(request)
            return self.parse_item_ids(response)
        except Exception as e:
            logging.error(f"Error fetching item IDs: {e}")
            return []

    def fetch_current_menu_items(self):
        try:
            request = "VIEW_CURRENT_MENU"
            response = send_request(request)
            return self.parse_item_details(response)
        except Exception as e:
            logging.error(f"Error fetching current menu items: {e}")
            return []

    def fetch_item_ids_with_names(self):
        try:
            request = "VIEW_MENU"
            response = send_request(request)
            return self.parse_item_details(response)
        except Exception as e:
            logging.error(f"Error fetching item IDs with names: {e}")
            return []

    def fetch_current_item_ids_with_names(self):
        try:
            request = "VIEW_CURRENT_MENU"
            response = send_request(request)
            return self.parse_item_details(response)
        except Exception as e:
            logging.error(f"Error fetching current item IDs with names: {e}")
            return []

    def parse_item_ids(self, response):
        items = response.split('\n')
        item_ids = []
        for item in items:
            if item.startswith("ID:"):
                item_id = int(item.split(',')[0].split(':')[1].strip())
                item_ids.append(item_id)
        return item_ids

    def parse_item_details(self, response):
        items = response.split('\n')
        item_details = []
        for item in items:
            if item.startswith("ID:"):
                parts = item.split(', ')
                item_id = int(parts[0].split(':')[1].strip())
                item_name = parts[1].split(':')[1].strip()
                item_details.append({'id': item_id, 'name': item_name})
        return item_details
