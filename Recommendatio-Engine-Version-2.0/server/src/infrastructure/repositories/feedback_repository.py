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
    @staticmethod
    def save_feedback_reply(feedback_reply):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = """
                INSERT INTO notification_replies (notification_id, employee_id, reply, reply_date, menu_id)
                VALUES (%s, %s, %s, NOW(), %s)
            """
            cursor.execute(query, (feedback_reply['notification_id'], feedback_reply['employee_id'], feedback_reply['reply'], feedback_reply['menu_id'] ))

            update_query = "UPDATE notifications SET is_read = 1 WHERE id = %s"
            cursor.execute(update_query, (feedback_reply['notification_id'],))
            
            db.commit()
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def get_feedback_replies():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT nr.notification_id, nr.employee_id, nr.reply, nr.reply_date
            FROM notification_replies nr
            JOIN notifications n ON nr.notification_id = n.id
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()
            db.close()