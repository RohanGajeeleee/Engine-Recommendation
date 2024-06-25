# server/src/infrastructure/repositories/feedback_repository.py
from src.infrastructure.db_config import get_db_connection
import mysql.connector
import logging
class FeedbackRepository:
    @staticmethod
    def add_feedback(employee_id, menu_id, comment, rating, feedback_date):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO feedback (employee_id, menu_id, comment, rating, feedback_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (employee_id, menu_id, comment, rating, feedback_date))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_all_feedback():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM feedback"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def can_give_feedback(employee_id, menu_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT feedback_given FROM choices WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            cursor.execute(query, (employee_id, menu_id, time_of_day))
            result = cursor.fetchone()
            logging.debug(f"Feedback check result: {result}")
            return result and not result[0]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def mark_feedback_given(employee_id, menu_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "UPDATE choices SET feedback_given = 1 WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            cursor.execute(query, (employee_id, menu_id, time_of_day))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def remove_choice(employee_id, menu_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "DELETE FROM choices WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            cursor.execute(query, (employee_id, menu_id, time_of_day))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()
