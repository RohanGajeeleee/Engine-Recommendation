import mysql.connector
from src.infrastructure.db_config import get_db_connection
from src.infrastructure.repositories.utility_repository import UtilityRepository
class MenuRepository:
    @staticmethod
    def add(menu_item):
        query = "INSERT INTO menu (name, price, availability, spice_level, food_category, dietary_type) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (menu_item.name, menu_item.price, menu_item.availability, menu_item.spice_level, menu_item.food_category, menu_item.dietary_type)
        MenuRepository._execute_query(query, params)

    @staticmethod
    def update(menu_item):
        updates, params = UtilityRepository.prepare_update_params(menu_item)
        if updates:
            query = f"UPDATE menu SET {', '.join(updates)} WHERE id = %s"
            MenuRepository._execute_query(query, tuple(params) + (menu_item.item_id,))

    @staticmethod
    def delete(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            UtilityRepository.delete_related_entries(item_id, cursor)
            query = "DELETE FROM menu WHERE id = %s"
            cursor.execute(query, (item_id,))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_all():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT id, name, price, availability FROM menu"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _execute_query(query, params=None):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def fetch_all_menu_items():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT m.id, m.name, m.price, m.availability,
                   AVG(f.rating) AS avg_rating, COUNT(f.id) AS feedback_count
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            GROUP BY m.id
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def get_item_name(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT name FROM menu WHERE id = %s"
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def fetch_all_menu_items_with_feedback():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT m.id, m.name, m.price, m.availability, m.spice_level, m.food_category, m.dietary_type, f.comment, f.rating
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            """
            cursor.execute(query)
            items = cursor.fetchall()
            for item in items:
                if item['rating'] is None:
                    item['rating'] = 0
            return items
        finally:
            cursor.close()
            db.close()

