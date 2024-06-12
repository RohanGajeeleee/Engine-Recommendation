import mysql.connector
from src.Database.db_config import get_db_connection

class ResetService:
    @staticmethod
    def reset_daily_data():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("TRUNCATE TABLE choices")
            cursor.execute("TRUNCATE TABLE recommendations")
            cursor.execute("DELETE FROM notifications WHERE is_read = 1")
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
