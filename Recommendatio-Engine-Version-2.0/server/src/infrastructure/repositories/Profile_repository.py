from src.infrastructure.db_config import get_db_connection
import mysql.connector
import logging
class ProfileRepository:
    @staticmethod
    def update(profile):
        db = get_db_connection()
        cursor = db.cursor()
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

            cursor.execute(query, tuple(params))
            db.commit()

            logging.info(f"Update successful for employee ID: {profile['employee_id']}")
        except Exception as e:
            logging.error(f"Error during update: {e}")
            raise
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_profile(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT dietary_preference, spice_level, cuisine_preference, sweet_tooth FROM employee_profiles WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            profile = cursor.fetchone()
            return profile
        finally:
            cursor.close()
            db.close()



    @staticmethod
    def create_profile(profile):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = """
            INSERT INTO employee_profiles (employee_id, dietary_preference, spice_level, cuisine_preference, sweet_tooth)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                profile['employee_id'],
                profile['dietary_preference'],
                profile['spice_level'],
                profile['cuisine_preference'],
                profile['sweet_tooth']
            ))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()
    