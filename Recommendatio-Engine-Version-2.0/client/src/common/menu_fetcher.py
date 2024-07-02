from common.network_utils import send_request
import logging

class MenuFetcher:
    @staticmethod
    def fetch_item_ids():
        try:
            request = "VIEW_MENU"
            response = send_request(request)
            return MenuFetcher.parse_item_ids(response)
        except Exception as e:
            logging.error(f"Error fetching item IDs: {e}")
            return []

    @staticmethod
    def fetch_current_menu_items():
        try:
            request = "VIEW_CURRENT_MENU"
            response = send_request(request)
            return MenuFetcher.parse_item_details(response)
        except Exception as e:
            logging.error(f"Error fetching current menu items: {e}")
            return []

    @staticmethod
    def fetch_item_ids_with_names():
        try:
            request = "VIEW_MENU"
            response = send_request(request)
            return MenuFetcher.parse_item_details(response)
        except Exception as e:
            logging.error(f"Error fetching item IDs with names: {e}")
            return []

    @staticmethod
    def fetch_current_item_ids_with_names():
        try:
            request = "VIEW_CURRENT_MENU"
            response = send_request(request)
            return MenuFetcher.parse_item_details(response)
        except Exception as e:
            logging.error(f"Error fetching current item IDs with names: {e}")
            return []

    @staticmethod
    def parse_item_ids(response):
        items = response.split('\n')
        item_ids = []
        for item in items:
            if item.startswith("ID:"):
                item_id = int(item.split(',')[0].split(':')[1].strip())
                item_ids.append(item_id)
        return item_ids

    @staticmethod
    def parse_item_details(response):
        items = response.split('\n')
        item_details = []
        for item in items:
            if item.startswith("ID:"):
                parts = item.split(', ')
                item_id = int(parts[0].split(':')[1].strip())
                item_name = parts[1].split(':')[1].strip()
                item_details.append({'id': item_id, 'name': item_name})
        return item_details
