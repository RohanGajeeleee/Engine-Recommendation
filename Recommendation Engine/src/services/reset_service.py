import mysql.connector
from src.Database.db_config import get_db_connection

class ResetService:
    @staticmethod
    def reset_daily_data():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            # Check if the next day menu is empty
            cursor.execute("SELECT COUNT(*) FROM next_day_menu")
            if cursor.fetchone()[0] == 0:
                return False

            # Move next day menu items to current menu
            cursor.execute("TRUNCATE TABLE current_menu")
            cursor.execute("INSERT INTO current_menu (menu_id) SELECT menu_id FROM next_day_menu")
            cursor.execute("TRUNCATE TABLE next_day_menu")

            # Clear daily choices and recommendations
            cursor.execute("TRUNCATE TABLE choices")
            cursor.execute("TRUNCATE TABLE recommendations")

            # Remove read notifications
            cursor.execute("DELETE FROM notifications WHERE is_read = 1")

            db.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
