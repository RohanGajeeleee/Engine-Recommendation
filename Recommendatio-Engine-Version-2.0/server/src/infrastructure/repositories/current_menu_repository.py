# server/src/infrastructure/repositories/current_menu_repository.py
from src.infrastructure.db_config import get_db_connection
import mysql.connector
import logging
class CurrentMenuRepository:
    @staticmethod
    def get_current_menu_items():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT cm.menu_id AS id, m.name, m.food_category, m.spice_level, m.dietary_type FROM current_menu cm JOIN menu m ON cm.menu_id = m.id"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def insert_choice(employee_id, item_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO choices (employee_id, menu_id, time_of_day) VALUES (%s, %s, %s)"
            cursor.execute(query, (employee_id, item_id, time_of_day))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def clear_current_menu():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "TRUNCATE TABLE current_menu"
            cursor.execute(query)
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def add_to_current_menu(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO current_menu (menu_id) VALUES (%s)"
            cursor.execute(query, (item_id,))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()
            
    @staticmethod
    def is_item_in_current_menu(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM current_menu WHERE menu_id = %s"
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()