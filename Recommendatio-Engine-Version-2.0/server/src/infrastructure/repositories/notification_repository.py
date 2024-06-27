from src.infrastructure.db_config import get_db_connection

class NotificationRepository:
    @staticmethod
    def get_all_employee_ids():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT employee_id FROM users WHERE role = 'employee'"
            cursor.execute(query)
            result = cursor.fetchall()
            return [row[0] for row in result]
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def add_notification(employee_id, message):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO notifications (employee_id, message, is_read, created_at) VALUES (%s, %s, %s, NOW())"
            cursor.execute(query, (employee_id, message, 0))
            db.commit()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_notifications_for_employee(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT id, message, created_at FROM notifications WHERE employee_id = %s AND is_read = 0"
            cursor.execute(query, (employee_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def mark_as_read(notification_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = %s", (notification_id,))
            db.commit()
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def get_feedback_requests(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT id, message 
            FROM notifications 
            WHERE employee_id = %s AND message LIKE 'We are trying to improve your experience with%'
            """
            cursor.execute(query, (employee_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()
    