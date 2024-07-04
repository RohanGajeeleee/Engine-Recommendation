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
        if menu_item.spice_level is not None:
            updates.append("spice_level = %s")
            params.append(menu_item.spice_level)
        if menu_item.food_category is not None:
            updates.append("food_category = %s")
            params.append(menu_item.food_category)
        if menu_item.dietary_type is not None:
            updates.append("dietary_type = %s")
            params.append(menu_item.dietary_type)

        return updates, params

    @staticmethod
    def delete_related_entries(item_id, cursor):
        related_tables = ['choices', 'feedback', 'current_menu']
        for table in related_tables:
            query = f"DELETE FROM {table} WHERE menu_id = %s"
            cursor.execute(query, (item_id,))
    @staticmethod
    def prepare_Profile_update_params(profile):
        updates = []
        params = []

        if profile.get("dietary_preference") is not None:
            updates.append("dietary_preference = %s")
            params.append(profile["dietary_preference"])

        if profile.get("spice_level") is not None:
            updates.append("spice_level = %s")
            params.append(profile["spice_level"])

        if profile.get("cuisine_preference") is not None:
            updates.append("cuisine_preference = %s")
            params.append(profile["cuisine_preference"])

        if profile.get("sweet_tooth") is not None:
            updates.append("sweet_tooth = %s")
            params.append(profile["sweet_tooth"])

        return updates, params