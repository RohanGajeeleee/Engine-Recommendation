import sys
import os
import hashlib
import mysql.connector
from src.Database.db_config import get_db_connection

class User:
    def __init__(self, employee_id, name=None, password=None, role=None):
        self.employee_id = employee_id
        self.name = name
        self.password = password
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(hashed_password, password):
        return hashed_password == hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        db = get_db_connection()
        cursor = db.cursor()
        hashed_password = self.hash_password(self.password)
        try:
            query = "INSERT INTO users (employee_id, name, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.employee_id, self.name, hashed_password, self.role))
            db.commit()
            print("User registered successfully")
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def authenticate(employee_id, password):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT password, role FROM users WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            if result and User.check_password(result[0], password):
                User.log_activity(employee_id, 'login', 'User logged in successfully')
                return result[1]
            else:
                User.log_activity(employee_id, 'login_failed', 'User login failed')
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
        return None

    @staticmethod
    def log_activity(employee_id, activity_type, description):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO user_activities (employee_id, activity_type, description) VALUES (%s, %s, %s)"
            cursor.execute(query, (employee_id, activity_type, description))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
