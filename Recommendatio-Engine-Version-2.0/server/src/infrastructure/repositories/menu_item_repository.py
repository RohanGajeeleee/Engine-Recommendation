import mysql.connector
from src.infrastructure.db_config import get_db_connection

class MenuItemRepository:
    @staticmethod
    def add(menu_item):
        query = "INSERT INTO menu (name, price, availability) VALUES (%s, %s, %s)"
        params = (menu_item.name, menu_item.price, menu_item.availability)
        MenuItemRepository._execute_query(query, params)

    @staticmethod
    def update(menu_item):
        updates, params = MenuItemRepository._prepare_update_params(menu_item)
        if updates:
            query = f"UPDATE menu SET {', '.join(updates)} WHERE id = %s"
            MenuItemRepository._execute_query(query, tuple(params) + (menu_item.item_id,))

    @staticmethod
    def delete(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            MenuItemRepository._delete_related_entries(item_id, cursor)
            query = "DELETE FROM menu WHERE id = %s"
            cursor.execute(query, (item_id,))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            raise err
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _delete_related_entries(item_id, cursor):
        related_tables = ['choices', 'feedback', 'recommendations', 'next_day_menu', 'current_menu']
        for table in related_tables:
            query = f"DELETE FROM {table} WHERE menu_id = %s"
            cursor.execute(query, (item_id,))

    @staticmethod
    def get_all():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT id, name, price, availability FROM menu"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _prepare_update_params(menu_item):
        updates = []
        params = []
        if menu_item.name is not None:
            updates.append("name = %s")
            params.append(menu_item.name)
        if menu_item.price is not None:
            updates.append("price = %s")
            params.append(menu_item.price)
        if menu_item.availability is not None:
            updates.append("availability = %s")
            params.append(menu_item.availability)
        return updates, params

    @staticmethod
    def _execute_query(query, params=None):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
            raise
        finally:
            cursor.close()
            db.close()
