import mysql.connector
from src.infrastructure.db_config import get_db_connection
from src.infrastructure.repositories.utility_repository import UtilityRepository
class MenuRepository:
    @staticmethod
    def add(menu_item):
        query = "INSERT INTO menu (name, price, availability) VALUES (%s, %s, %s)"
        params = (menu_item.name, menu_item.price, menu_item.availability)
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
