from src.infrastructure.db_config import get_db_connection
import mysql.connector
class ChoiceRepository:
    @staticmethod
    def get_choices_by_employee_and_time(employee_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
                SELECT c.menu_id, m.name 
                FROM choices c
                JOIN menu m ON c.menu_id = m.id
                WHERE c.employee_id = %s AND c.time_of_day = %s AND c.feedback_given = 0
            """
            cursor.execute(query, (employee_id, time_of_day))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def item_already_chosen(employee_id, item_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM choices WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            cursor.execute(query, (employee_id, item_id, time_of_day))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
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