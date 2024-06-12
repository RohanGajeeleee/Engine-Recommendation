import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# src/user.py

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
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def check_password(hashed_password, password):
        """Check if the provided password matches the hashed password."""
        return hashed_password == hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        """Register a new user with hashed password."""
        db = get_db_connection()
        cursor = db.cursor()
        hashed_password = self.hash_password(self.password)
        try:
            query = "INSERT INTO users (employee_id, name, password, role) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (self.employee_id, self.name, hashed_password, self.role))
            db.commit()
            print("User registered successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def authenticate(employee_id, password):
        """Authenticate a user by comparing hashed password."""
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT password, role FROM users WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            if result and User.check_password(result[0], password):
                return result[1]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
        return None
