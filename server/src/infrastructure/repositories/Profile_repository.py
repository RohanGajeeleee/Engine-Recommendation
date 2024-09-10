from src.infrastructure.db_config import get_db_connection
import mysql.connector
import logging

class ProfileRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def update(self, profile):
        try:
            updates = []
            params = []

            for key, value in profile.items():
                if value is not None and key != 'employee_id':
                    updates.append(f"{key} = %s")
                    params.append(value)

            if not updates:
                raise ValueError("No fields to update")

            query = f"UPDATE employee_profiles SET {', '.join(updates)} WHERE employee_id = %s"
            params.append(profile['employee_id'])

            logging.info(f"Executing query: {query}")
            logging.info(f"With parameters: {params}")

            self.cursor.execute(query, tuple(params))
            self.db.commit()

            logging.info(f"Update successful for employee ID: {profile['employee_id']}")
        except Exception as e:
            logging.error(f"Error during update: {e}")
            raise

    def get_profile(self, employee_id):
        try:
            query = "SELECT dietary_preference, spice_level, cuisine_preference, sweet_tooth FROM employee_profiles WHERE employee_id = %s"
            self.cursor.execute(query, (employee_id,))
            profile = self.cursor.fetchone()
            return profile
        except mysql.connector.Error as err:
            logging.error(f"Error: {err}")
            return None

    def create_profile(self, profile):
        try:
            query = """
            INSERT INTO employee_profiles (employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (
                profile['employee_id'],
                profile['dietary_preference'],
                profile['spice_level'],
                profile['cuisine_preference'],
                profile['sweet_tooth']
            ))
            self.db.commit()
        except mysql.connector.Error as err:
            self.db.rollback()
            logging.error(f"Error: {err}")
            raise
