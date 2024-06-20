import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mysql.connector
from src.Database.db_config import get_db_connection

class MenuItem:
    def __init__(self, item_id=None, name=None, price=None, availability=None):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.availability = availability

    def add(self):
        query = "INSERT INTO menu (name, price, availability) VALUES (%s, %s, %s)"
        params = (self.name, self.price, self.availability)
        self._execute_query(query, params)

    def update(self):
        updates, params = self._prepare_update_params()
        if updates:
            query = f"UPDATE menu SET {', '.join(updates)} WHERE id = %s"
            self._execute_query(query, tuple(params) + (self.item_id,))

    def delete(self):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "DELETE FROM choices WHERE menu_id = %s"
            cursor.execute(query, (self.item_id,))
            db.commit()

            query = "DELETE FROM feedback WHERE menu_id = %s"
            cursor.execute(query, (self.item_id,))
            db.commit()

            query = "DELETE FROM recommendations WHERE menu_id = %s"
            cursor.execute(query, (self.item_id,))
            db.commit()

            query = "DELETE FROM next_day_menu WHERE menu_id = %s"
            cursor.execute(query, (self.item_id,))
            db.commit()

            query = "DELETE FROM current_menu WHERE menu_id = %s"
            cursor.execute(query, (self.item_id,))
            db.commit()

            query = "DELETE FROM menu WHERE id = %s"
            cursor.execute(query, (self.item_id,))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()
            
    @staticmethod
    def get_all_items():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT 
                m.id, m.name, m.price, m.availability, 
                AVG(f.rating) AS avg_rating, 
                COUNT(f.id) AS feedback_count 
            FROM 
                menu m 
            LEFT JOIN 
                feedback f 
            ON 
                m.id = f.menu_id 
            GROUP BY 
                m.id, m.name, m.price, m.availability
            """
            cursor.execute(query)
            items = cursor.fetchall()
            return items
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    def _prepare_update_params(self):
        updates = []
        params = []
        if self.name:
            updates.append("name = %s")
            params.append(self.name)
        if self.price:
            updates.append("price = %s")
            params.append(self.price)
        if self.availability:
            updates.append("availability = %s")
            params.append(self.availability)
        return updates, params

    @staticmethod
    def _execute_query(query, params=None):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()
