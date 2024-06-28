# server/src/application/services/menu_service.py

import logging
from src.infrastructure.repositories.menu_repository import MenuRepository
from src.domain.models.menu_item import MenuItem

logging.basicConfig(level=logging.INFO)

class MenuService:
    @staticmethod
    def list_items():
        try:
            items = MenuRepository.get_all()
            logging.info("Listed menu items")
            return items if items else "No menu items available."
        except Exception as e:
            logging.error(f"Error listing items: {e}")
            return f"Error listing items: {e}"

    @staticmethod
    def add_item(name, price, availability, spice_level, food_category, dietary_type):
        try:
            menu_item = MenuItem(
                name=name,
                price=price,
                availability=availability,
                spice_level=spice_level,
                food_category=food_category,
                dietary_type=dietary_type
            )
            MenuRepository.add(menu_item)
            logging.info(f"Added menu item: {name}")
            return "Menu item added successfully"
        except Exception as e:
            logging.error(f"Error adding item: {e}")
            return f"Error adding item: {e}"
    @staticmethod
    def update_item(item_id, name=None, price=None, availability=None, spice_level=None, food_category=None, dietary_type=None):
        try:
            menu_item = MenuItem(item_id=item_id, name=name, price=price, availability=availability, spice_level=spice_level, food_category=food_category, dietary_type=dietary_type)
            MenuRepository.update(menu_item)
            logging.info(f"Updated menu item ID: {item_id}")
            return "Menu item updated successfully"
        except Exception as e:
            logging.error(f"Error updating item: {e}")
            return f"Error updating item: {e}"

    @staticmethod
    def delete_item(item_id):
        try:
            MenuRepository.delete(item_id)
            logging.info(f"Deleted menu item ID: {item_id}")
            return "Menu item deleted successfully"
        except Exception as e:
            logging.error(f"Error deleting item: {e}")
            return f"Error deleting item: {e}"
    @staticmethod
    def get_item_name(item_id):
        return MenuRepository.get_item_name(item_id)