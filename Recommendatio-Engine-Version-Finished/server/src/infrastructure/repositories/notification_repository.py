from src.infrastructure.db_config import get_db_connection
import mysql.connector

class NotificationRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def get_all_employee_ids(self):
        try:
            query = "SELECT employee_id FROM users WHERE role = 'employee'"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [row['employee_id'] for row in result]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def add_notification(self, employee_id, message):
        try:
            query = "INSERT INTO notifications (employee_id, message, is_read, created_at) VALUES (%s, %s, %s, NOW())"
            self.cursor.execute(query, (employee_id, message, 0))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            print(f"Error: {err}")
            raise

    def get_notifications_for_employee(self, employee_id):
        try:
            query = "SELECT id, message, created_at FROM notifications WHERE employee_id = %s AND is_read = 0"
            self.cursor.execute(query, (employee_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def mark_as_read(self, notification_id):
        try:
            query = "UPDATE notifications SET is_read = 1 WHERE id = %s"
            self.cursor.execute(query, (notification_id,))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            print(f"Error: {err}")
            raise

    def get_feedback_requests(self, employee_id):
        try:
            query = """
            SELECT id, message 
            FROM notifications 
            WHERE employee_id = %s AND message LIKE 'We are trying to improve your experience with%'
            """
            self.cursor.execute(query, (employee_id,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
