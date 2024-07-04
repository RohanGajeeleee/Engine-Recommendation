import mysql.connector
from src.domain.models.user import User
from src.infrastructure.db_config import get_db_connection

class UserRepository:
    def __init__(self):
        self.db = get_db_connection()

    def save(self, user):
        cursor = self.db.cursor()
        try:
            query = "INSERT INTO users (employee_id, name, password, role) VALUES (%s, %s, %s, %s)"
            hashed_password = User.hash_password(user.password)  
            cursor.execute(query, (user.employee_id, user.name, hashed_password, user.role))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            raise err
        finally:
            cursor.close()

    def find_by_id(self, employee_id):
        cursor = self.db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            if result:
                return User(**result)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
        return None

    def close(self):
        self.db.close()
