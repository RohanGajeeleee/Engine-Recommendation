import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.common.menu_item_checker import MenuItemChecker
from src.common.input_validation import InputValidator
from src.common.RequestBuilder import MenuRequestBuilder
from src.common.network_utils import send_request

class MenuManager:
    def __init__(self):
        self.input_validator = InputValidator()
        self.menu_item_checker = MenuItemChecker()

    def add_item(self):
        name = self.input_validator.get_valid_input("Enter item name: ")
        price = self.input_validator.get_valid_price("Enter item price: ")
        availability = self.input_validator.get_valid_availability("Enter availability (1 for Available, 2 for Unavailable): ")
        spice_level = self.input_validator.get_valid_spice_level("Enter spice level (1 for Low, 2 for Medium, 3 for High): ")
        food_category = self.input_validator.get_valid_food_category("Enter food category (1 for North Indian, 2 for South Indian, 3 for Other, 4 for Dessert): ")
        dietary_type = self.input_validator.get_valid_dietary_type("Enter dietary type (1 for Vegetarian, 2 for Non-Vegetarian, 3 for Eggetarian): ")
        
        request = MenuRequestBuilder.add_item_request(name, price, availability, spice_level, food_category, dietary_type)
        response = send_request(request)
        print(response)
        return True

    def update_item(self):
        self.view_menu()
        item_id = self.menu_item_checker.get_existing_item_id("Enter item ID to update: ")
        name = self.input_validator.get_valid_input("Enter new name (or leave blank to keep current): ", allow_empty=True)
        price = self.input_validator.get_valid_price("Enter new price (or leave blank to keep current): ", allow_empty=True)
        availability = self.input_validator.get_valid_availability("Enter new availability (1 for Available, 2 for Unavailable, or leave blank to keep current): ", allow_empty=True)
        spice_level = self.input_validator.get_valid_spice_level("Enter new spice level (1 for Low, 2 for Medium, 3 for High, or leave blank to keep current): ", allow_empty=True)
        food_category = self.input_validator.get_valid_food_category("Enter new food category (1 for North Indian, 2 for South Indian, 3 for Other, 4 for Dessert, or leave blank to keep current): ", allow_empty=True)
        dietary_type = self.input_validator.get_valid_dietary_type("Enter new dietary type (1 for Vegetarian, 2 for Non-Vegetarian, 3 for Eggetarian, or leave blank to keep current): ", allow_empty=True)
        
        request = MenuRequestBuilder.update_item_request(item_id, name, price, availability, spice_level, food_category, dietary_type)
        response = send_request(request)
        print(response)
        return True

    def delete_item(self):
        self.view_menu()
        item_id = self.menu_item_checker.get_existing_item_id("Enter item ID to delete: ")
        request = MenuRequestBuilder.delete_item_request(item_id)
        response = send_request(request)
        print(response)
        return True

    def view_menu(self):
        request = MenuRequestBuilder.view_menu_request()
        response = send_request(request)
        print(response)
        return True
