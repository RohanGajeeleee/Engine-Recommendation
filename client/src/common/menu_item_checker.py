import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from common.menu_fetcher import MenuFetcher
from common.choice_fetcher import ChoiceFetcher
from common.menu_validator import MenuValidator
from common.menu_utils import MenuUtils

class MenuItemChecker:
    def __init__(self):
        self.menu_fetcher = MenuFetcher()
        self.choice_fetcher = ChoiceFetcher()
        self.menu_validator = MenuValidator()
        self.menu_utils = MenuUtils()

    def fetch_item_ids(self):
        return self.menu_fetcher.fetch_item_ids()

    def fetch_current_menu_items(self):
        return self.menu_fetcher.fetch_current_menu_items()

    def fetch_item_ids_with_names(self):
        return self.menu_fetcher.fetch_item_ids_with_names()

    def fetch_current_item_ids_with_names(self):
        return self.menu_fetcher.fetch_current_item_ids_with_names()

    def fetch_user_choices(self, employee_id, time_of_day):
        return self.choice_fetcher.fetch_user_choices(employee_id, time_of_day)

    def get_existing_item_id(self, prompt):
        return self.menu_validator.get_existing_item_id(prompt, self.fetch_item_ids_with_names)

    def get_existing_choice_id(self, user_choices, prompt):
        return self.menu_validator.get_existing_choice_id(user_choices, prompt)

    def get_existing_current_item_id(self, prompt):
        return self.menu_validator.get_existing_current_item_id(prompt, self.fetch_current_item_ids_with_names)

    def parse_available_items(self, menu_items):
        parsed_items = self.menu_utils.parse_available_items(menu_items)
        return parsed_items

    def is_item_available(self, available_items, item_id):
        availability = self.menu_utils.is_item_available(available_items, item_id)
        return availability
