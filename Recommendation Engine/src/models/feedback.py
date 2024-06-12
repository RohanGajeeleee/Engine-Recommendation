import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from src.Database.db_config import get_db_connection

class Feedback:
    def __init__(self, employee_id=None, menu_id=None, comment=None, rating=None, feedback_date=None):
        self.employee_id = employee_id
        self.menu_id = menu_id
        self.comment = comment
        self.rating = rating
        self.feedback_date = feedback_date

    def add(self):
        query = "INSERT INTO feedback (employee_id, menu_id, comment, rating, feedback_date) VALUES (%s, %s, %s, %s, CURDATE())"
        params = (self.employee_id, self.menu_id, self.comment, self.rating)
        self._execute_query(query, params)
        print("Feedback added successfully")

    @staticmethod
    def view():
        query = "SELECT employee_id, menu_id, comment, rating, feedback_date FROM feedback"
        results = Feedback._execute_query(query)
        if results:
            for row in results:
                print(f"Employee ID: {row['employee_id']}, Menu ID: {row['menu_id']}, Comment: {row['comment']}, Rating: {row['rating']}, Date: {row['feedback_date']}")
        else:
            print("No feedback available")

    @staticmethod
    def _execute_query(query, params=None):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True if 'SELECT' in query else False)
        try:
            cursor.execute(query, params)
            if 'SELECT' in query:
                return cursor.fetchall()
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
