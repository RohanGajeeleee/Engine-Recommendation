import mysql.connector
from src.infrastructure.db_config import get_db_connection

class ValidationRepository:
    def __init__(self):
        self.db = get_db_connection()

    def is_valid_item_id(self, item_id):
        cursor = self.db.cursor()
        try:
            query = "SELECT COUNT(*) FROM menu WHERE id = %s"
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()

    def close(self):
        self.db.close()
