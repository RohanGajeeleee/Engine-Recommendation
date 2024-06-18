import mysql.connector
from src.Database.db_config import get_db_connection
from src.models.feedback import Feedback
from src.models.recommendations import Recommendation
from src.models.notifications import Notification

class EmployeeService:
    
    @staticmethod
    def get_choices_for_feedback(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT c.menu_id, m.name 
            FROM choices c 
            JOIN menu m ON c.menu_id = m.id 
            WHERE c.employee_id = %s AND c.feedback_given = 0
            """
            cursor.execute(query, (employee_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def mark_feedback_given(employee_id, menu_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "UPDATE choices SET feedback_given = 1 WHERE employee_id = %s AND menu_id = %s"
            cursor.execute(query, (employee_id, menu_id))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    
    @staticmethod
    def fetch_notifications(employee_id):
        notifications = Notification.fetch_and_clear_notifications(employee_id)
        return notifications
    
    @staticmethod
    def fetch_recommended_items():
        return Recommendation.fetch_recommended_items()

    @staticmethod
    def has_already_chosen(employee_id):
        return Recommendation.has_already_chosen(employee_id)
    
    @staticmethod
    def choose_recommended_item(employee_id, menu_id):
        Recommendation.choose_recommended_item(employee_id, menu_id)
