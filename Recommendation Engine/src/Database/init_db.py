import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import mysql.connector
from src.Database.db_config import get_db_connection
from src.models.menu_management import MenuItem

def clear_database():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE feedback")
        cursor.execute("TRUNCATE TABLE notifications")
        cursor.execute("TRUNCATE TABLE recommendations")
        cursor.execute("TRUNCATE TABLE choices")
        cursor.execute("TRUNCATE TABLE users")
        cursor.execute("TRUNCATE TABLE menu")
        cursor.execute("ALTER TABLE feedback AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE notifications AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE recommendations AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE choices AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE menu AUTO_INCREMENT = 1")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        db.close()

def insert_initial_data():
    file_path = os.path.join(os.path.dirname(__file__), 'initial_data.json')
    with open(file_path, 'r') as file:
        data = json.load(file)

    for item in data['menu_items']:
        new_item = MenuItem(name=item['name'], price=item['price'], availability=item['availability'])
        new_item.add()

if __name__ == "__main__":
    clear_database()
    insert_initial_data()
