import sys
import os
import mysql.connector
from src.domain.models.user import User
from src.infrastructure.db_config import get_db_connection

class UserRepository:
    @staticmethod
    def save(user):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO users (employee_id, name, password, role) VALUES (%s, %s, %s, %s)"
            hashed_password = User.hash_password(user.password)  
            cursor.execute(query, (user.employee_id, user.name, hashed_password, user.role))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def find_by_id(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
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
            db.close()
        return None
