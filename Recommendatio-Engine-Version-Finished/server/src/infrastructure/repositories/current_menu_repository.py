from src.infrastructure.db_config import get_db_connection
import mysql.connector
import logging

class CurrentMenuRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def get_current_menu_items(self):
        try:
            query = """
                SELECT cm.menu_id AS id, m.name, m.food_category, m.spice_level, m.dietary_type 
                FROM current_menu cm 
                JOIN menu m ON cm.menu_id = m.id
            """
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []

    def insert_choice(self, employee_id, item_id, time_of_day):
        try:
            query = "INSERT INTO choices (employee_id, menu_id, time_of_day) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (employee_id, item_id, time_of_day))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def clear_current_menu(self):
        try:
            query = "TRUNCATE TABLE current_menu"
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def add_to_current_menu(self, item_id):
        try:
            query = "INSERT INTO current_menu (menu_id) VALUES (%s)"
            self.cursor.execute(query, (item_id,))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def is_item_in_current_menu(self, item_id):
        try:
            query = "SELECT COUNT(*) FROM current_menu WHERE menu_id = %s"
            self.cursor.execute(query, (item_id,))
            result = self.cursor.fetchone()
            return result['COUNT(*)'] > 0
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return False
