from src.infrastructure.db_config import get_db_connection
from src.infrastructure.repositories.utility_repository import UtilityRepository
import mysql.connector
import logging

class MenuRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)
        self.utility_repository = UtilityRepository()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def add(self, menu_item):
        query = "INSERT INTO menu (name, price, availability, spice_level, food_category, dietary_type) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (menu_item.name, menu_item.price, menu_item.availability, menu_item.spice_level, menu_item.food_category, menu_item.dietary_type)
        self._execute_query(query, params)

    def update(self, menu_item):
        updates, params = self.utility_repository.prepare_update_params(menu_item)  
        if updates:
            query = f"UPDATE menu SET {', '.join(updates)} WHERE id = %s"
            self._execute_query(query, tuple(params) + (menu_item.item_id,))

    def delete(self, item_id):
        try:
            self.utility_repository.delete_related_entries(item_id)
            query = "DELETE FROM menu WHERE id = %s"
            self.cursor.execute(query, (item_id,))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise err

    def get_all(self):
        try:
            query = "SELECT id, name, price, availability FROM menu"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []

    def _execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def fetch_all_menu_items(self):
        try:
            query = """
            SELECT m.id, m.name, m.price, m.availability,
                   AVG(f.rating) AS avg_rating, COUNT(f.id) AS feedback_count
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            GROUP BY m.id
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []

    def get_item_name(self, item_id):
        try:
            query = "SELECT name FROM menu WHERE id = %s"
            self.cursor.execute(query, (item_id,))
            result = self.cursor.fetchone()
            if result:
                return result['name']
            return None
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return None

    def fetch_all_menu_items_with_feedback(self):
        try:
            query = """
            SELECT m.id, m.name, m.price, m.availability, m.spice_level, m.food_category, m.dietary_type, f.comment, f.rating
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            """
            self.cursor.execute(query)
            items = self.cursor.fetchall()
            for item in items:
                if item['rating'] is None:
                    item['rating'] = 0
            return items
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []
