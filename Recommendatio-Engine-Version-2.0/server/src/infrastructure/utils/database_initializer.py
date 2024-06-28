import os
import json
import mysql.connector
import sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.infrastructure.db_config import get_db_connection

logging.basicConfig(level=logging.DEBUG)

def clear_database():
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute("TRUNCATE TABLE feedback")
        cursor.execute("TRUNCATE TABLE notifications")
        cursor.execute("TRUNCATE TABLE recommendations")
        cursor.execute("TRUNCATE TABLE choices")
        cursor.execute("TRUNCATE TABLE discarded_items")
        cursor.execute("TRUNCATE TABLE current_menu")
        cursor.execute("TRUNCATE TABLE notification_replies")
        cursor.execute("TRUNCATE TABLE menu")
        cursor.execute("ALTER TABLE feedback AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE discarded_items AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE notification_replies AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE notifications AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE recommendations AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE choices AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE current_menu AUTO_INCREMENT = 1")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        db.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error clearing database: {err}")
    finally:
        cursor.close()
        db.close()

def insert_initial_data():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'initial_data.json')

    if not os.path.isfile(file_path):
        logging.error(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        data = json.load(file)

    db = get_db_connection()
    cursor = db.cursor()
    try:
        for item in data['menu_items']:
            cursor.execute(
                "INSERT INTO menu (name, price, availability, spice_level, food_category, dietary_type) VALUES (%s, %s, %s, %s, %s, %s)",
                (item['name'], item['price'], item['availability'], item['spice_level'], item['food_category'], item['dietary_type'])
            )
        for item in data['current_menu_items']:
            cursor.execute("INSERT INTO current_menu (menu_id) VALUES (%s)", (item['menu_id'],))

        db.commit()
    except mysql.connector.Error as err:
        logging.error(f"Error inserting initial data: {err}")
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    clear_database()
    insert_initial_data()
