# src/menu_management.py

import sys
import os

# Ensure the src directory is in the Python path
from src.models.menu_management import MenuItem

class MenuItemService:
    @staticmethod
    def add_item(name, price, availability):
        menu_item = MenuItem(name=name, price=price, availability=availability)
        menu_item.add()

    @staticmethod
    def update_item(item_id, name=None, price=None, availability=None):
        menu_item = MenuItem(item_id=item_id, name=name, price=price, availability=availability)
        menu_item.update()

    @staticmethod
    def delete_item(item_id):
        menu_item = MenuItem(item_id=item_id)
        menu_item.delete()
