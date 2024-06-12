# src/menu_management.py

import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from src.Database.db_config import get_db_connection

class MenuItem:
    def __init__(self, item_id=None, name=None, price=None, availability=None):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.availability = availability

    def add(self):
        """Add a new menu item."""
        query = "INSERT INTO menu (name, price, availability) VALUES (%s, %s, %s)"
        params = (self.name, self.price, self.availability)
        self._execute_query(query, params)
        print("Menu item added successfully")

    def update(self):
        """Update an existing menu item."""
        updates, params = self._prepare_update_params()
        if updates:
            query = f"UPDATE menu SET {', '.join(updates)} WHERE id = %s"
            self._execute_query(query, tuple(params) + (self.item_id,))
            print("Menu item updated successfully")
        else:
            print("No updates provided.")

    def delete(self):
        """Delete a menu item."""
        query = "DELETE FROM menu WHERE id = %s"
        params = (self.item_id,)
        self._execute_query(query, params)
        print("Menu item deleted successfully")

    def _prepare_update_params(self):
        """Prepare update parameters."""
        updates = []
        params = []
        if self.name:
            updates.append("name = %s")
            params.append(self.name)
        if self.price:
            updates.append("price = %s")
            params.append(self.price)
        if self.availability:
            updates.append("availability = %s")
            params.append(self.availability)
        return updates, params

    @staticmethod
    def _execute_query(query, params=None):
        """Execute a database query."""
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
