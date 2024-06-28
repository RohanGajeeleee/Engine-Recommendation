# client/src/common/menu_fetcher.py

from common.network_utils import send_request
import logging
class MenuFetcher:
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
    def fetch_current_menu_items():
        request = "VIEW_CURRENT_MENU"
        response = send_request(request)
        items = response.split('\n')
        current_menu_items = []
        for item in items:
            if item.startswith("ID:"):
                parts = item.split(', ')
                item_id = int(parts[0].split(':')[1].strip())
                item_name = parts[1].split(':')[1].strip()
                current_menu_items.append({'id': item_id, 'name': item_name})
        return current_menu_items

    @staticmethod
    def fetch_item_ids_with_names():
        request = "VIEW_MENU"
        response = send_request(request)
        items = response.split('\n')
        item_details = []
        for item in items:
            if item.startswith("ID:"):
                parts = item.split(',')
                item_id = int(parts[0].split(':')[1].strip())
                name = parts[1].split(':')[1].strip()
                item_details.append({'id': item_id, 'name': name})
        return item_details

    @staticmethod
    def fetch_current_item_ids_with_names():
        request = "VIEW_CURRENT_MENU"
        response = send_request(request)
        items = response.split('\n')
        item_details = []
        for item in items:
            if item.startswith("ID:"):
                parts = item.split(',')
                item_id = int(parts[0].split(':')[1].strip())
                name = parts[1].split(':')[1].strip()
                item_details.append({'id': item_id, 'name': name})
        return item_details
