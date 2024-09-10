from src.infrastructure.db_config import get_db_connection
import mysql.connector
import logging

class FeedbackRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def add_feedback(self, employee_id, menu_id, comment, rating, feedback_date):
        try:
            query = "INSERT INTO feedback (employee_id, menu_id, comment, rating, feedback_date) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(query, (employee_id, menu_id, comment, rating, feedback_date))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def get_all_feedback(self):
        try:
            query = "SELECT * FROM feedback"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []

    def can_give_feedback(self, employee_id, menu_id, time_of_day):
        try:
            query = "SELECT feedback_given FROM choices WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            self.cursor.execute(query, (employee_id, menu_id, time_of_day))
            result = self.cursor.fetchone()
            return result and not result['feedback_given']
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return False

    def mark_feedback_given(self, employee_id, menu_id, time_of_day):
        try:
            query = "UPDATE choices SET feedback_given = 1 WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            self.cursor.execute(query, (employee_id, menu_id, time_of_day))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def remove_choice(self, employee_id, menu_id, time_of_day):
        try:
            query = "DELETE FROM choices WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            self.cursor.execute(query, (employee_id, menu_id, time_of_day))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def save_feedback_reply(self, feedback_reply):
        try:
            query = """
                INSERT INTO notification_replies (notification_id, employee_id, reply, reply_date, menu_id)
                VALUES (%s, %s, %s, NOW(), %s)
            """
            self.cursor.execute(query, (feedback_reply['notification_id'], feedback_reply['employee_id'], feedback_reply['reply'], feedback_reply['menu_id']))

            update_query = "UPDATE notifications SET is_read = 1 WHERE id = %s"
            self.cursor.execute(update_query, (feedback_reply['notification_id'],))
            
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise

    def get_feedback_replies(self):
        try:
            query = """
            SELECT nr.notification_id, nr.employee_id, nr.reply, nr.reply_date
            FROM notification_replies nr
            JOIN notifications n ON nr.notification_id = n.id
            """
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return []
