
import logging
from src.infrastructure.repositories.current_menu_repository import CurrentMenuRepository
from src.infrastructure.repositories.Choice_Repository import ChoiceRepository
from src.infrastructure.repositories.validation_repository import ValidationRepository
from src.application.services.profile_service import ProfileService
logging.basicConfig(level=logging.INFO)

class CurrentMenuService:
    @staticmethod
    def get_current_menu():
        try:
            current_menu_items = CurrentMenuRepository.get_current_menu_items()
            logging.info("Fetched current menu items")
            return current_menu_items
        except Exception as e:
            logging.error(f"Error fetching current menu items: {e}")
            return []

    @staticmethod
    def sort_menu_items_by_preferences(menu_items, preferences):
        def preference_score(item):
            score = 0
            if item['dietary_type'] == preferences['dietary_preference']:
                score += 5  
            if item['spice_level'] == preferences['spice_level']:
                score += 3  
            if item['food_category'] == preferences['cuisine_preference']:
                score += 2  
            if item['food_category'] == 'Dessert' and preferences['sweet_tooth'] == 'Yes':
                score += 1  
            return score

        sorted_items = sorted(menu_items, key=preference_score, reverse=True)
        return sorted_items
        

    @staticmethod
    def get_sorted_menu_items_by_preferences(employee_id):

        user_preferences = ProfileService.get_user_preferences(employee_id)
        if not user_preferences:
            return f"No preferences found for employee ID {employee_id}"

        current_menu_items = CurrentMenuService.get_current_menu()
        if isinstance(current_menu_items, str):  
            return current_menu_items

        sorted_menu_items = CurrentMenuService.sort_menu_items_by_preferences(current_menu_items, user_preferences)

        response = "\nRecommended Menu Items:\n"
        for item in sorted_menu_items:
            response += f"ID: {item['id']}, Name: {item['name']}\n"
        return response 
    @staticmethod
    def choose_recommended_item(employee_id, item_id, time_of_day):
        try:
            if not ValidationRepository.is_valid_item_id(item_id):
                return f"Item ID {item_id} is not valid."
            if ChoiceRepository.item_already_chosen(employee_id, item_id, time_of_day):
                return f"Item ID {item_id} has already been chosen for {time_of_day}."
            CurrentMenuRepository.insert_choice(employee_id, item_id, time_of_day)
            logging.info(f"Employee {employee_id} chose recommended item ID: {item_id} for {time_of_day}")
            return "Recommended item chosen successfully"
        except Exception as e:
            logging.error(f"Error choosing recommended item: {e}")
            return f"Error choosing recommended item: {e}"
    @staticmethod
    def clear_current_menu():
        try:
            CurrentMenuRepository.clear_current_menu()
            logging.info("Cleared current menu")
            return "Current menu cleared"
        except Exception as e:
            logging.error(f"Error clearing current menu: {e}")
            return f"Error clearing current menu: {e}"

    @staticmethod
    def add_item_to_current_menu(item_id):
        try:
            if not ValidationRepository.is_valid_item_id(item_id):
                return f"Item ID {item_id} is not valid."
            if CurrentMenuRepository.is_item_in_current_menu(item_id):
                return f"Item ID {item_id} is already in the current menu."
            CurrentMenuRepository.add_to_current_menu(item_id)
            logging.info(f"Added item ID: {item_id} to current menu")
            return "Item added to current menu successfully"
        except Exception as e:
            logging.error(f"Error adding item to current menu: {e}")
            return f"Error adding item to current menu: {e}"
    @staticmethod
    def finalize_current_menu():
        try:
            new_menu_items = CurrentMenuRepository.get_current_menu_items()
            if not new_menu_items:
                return "No items in the current menu. Please add at least one item."
            logging.info("Finalized current menu")
            return new_menu_items
        except Exception as e:
            logging.error(f"Error finalizing current menu: {e}")
            return f"Error finalizing current menu: {e}"
  