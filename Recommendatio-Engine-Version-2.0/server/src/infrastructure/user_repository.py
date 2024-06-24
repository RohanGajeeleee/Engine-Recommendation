import sys
import os

# Adjust the path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.infrastructure.db_config import get_db_connection
from src.domain.models.user import User

class UserRepository:
    def find_by_id(self, employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            if result:
                return User(**result)
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
            db.close()

    def save(self, user):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO users (employee_id, name, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (user.employee_id, user.name, user.password, user.role))
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return False
        finally:
            cursor.close()
            db.close()
