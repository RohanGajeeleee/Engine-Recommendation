import mysql.connector
from src.infrastructure.db_config import get_db_connection

class UtilityRepository:
    @staticmethod
    def prepare_update_params(menu_item):
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
    def delete_related_entries(item_id, cursor):
        related_tables = ['choices', 'feedback', 'recommendations', 'next_day_menu', 'current_menu']
        for table in related_tables:
            query = f"DELETE FROM {table} WHERE menu_id = %s"
            cursor.execute(query, (item_id,))
