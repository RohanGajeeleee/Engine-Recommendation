from src.infrastructure.db_config import get_db_connection
import mysql.connector

class ChoiceRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def get_choices_by_employee_and_time(self, employee_id, time_of_day):
        try:
            query = """
                SELECT c.menu_id, m.name 
                FROM choices c
                JOIN menu m ON c.menu_id = m.id
                WHERE c.employee_id = %s AND c.time_of_day = %s AND c.feedback_given = 0
            """
            self.cursor.execute(query, (employee_id, time_of_day))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def item_already_chosen(self, employee_id, item_id, time_of_day):
        try:
            query = "SELECT COUNT(*) FROM choices WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            self.cursor.execute(query, (employee_id, item_id, time_of_day))
            result = self.cursor.fetchone()
            return result['COUNT(*)'] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def insert_choice(self, employee_id, item_id, time_of_day):
        try:
            query = "INSERT INTO choices (employee_id, menu_id, time_of_day) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (employee_id, item_id, time_of_day))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            print(f"Error: {err}")
            raise
