from src.infrastructure.db_config import get_db_connection
from src.infrastructure.repositories.menu_repository import MenuRepository
from src.infrastructure.repositories.utility_repository import UtilityRepository

class DiscardRepository:
    def __init__(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor(dictionary=True)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    def item_exists_in_discard(self, item_id):
        try:
            query = "SELECT COUNT(*) FROM discarded_items WHERE id = %s"
            self.cursor.execute(query, (item_id,))
            result = self.cursor.fetchone()
            return result['COUNT(*)'] > 0
        except Exception as e:
            print(f"Error: {e}")
            return False

    def get_discarded_items(self):
        try:
            query = "SELECT id, name, price, availability FROM discarded_items"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return []

    def restore_item(self, item_id):
        try:
            menu_id = self._get_menu_id(item_id)
            if not menu_id:
                return "Item not found in discarded items."
            
            self._insert_into_menu(item_id)
            self._delete_from_discarded_items(item_id)
            self._delete_related_notifications(menu_id)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback() 
            print(f"Error: {e}")
            raise e

    def _get_menu_id(self, item_id):
        try:
            query = "SELECT menu_id FROM discarded_items WHERE id = %s"
            self.cursor.execute(query, (item_id,))
            result = self.cursor.fetchone()
            return result['menu_id'] if result else None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _insert_into_menu(self, item_id):
        try:
            query = """
            INSERT INTO menu (name, price, availability, spice_level, food_category, dietary_type) 
            SELECT name, price, availability, spice_level, food_category, dietary_type FROM discarded_items WHERE id = %s
            """
            self.cursor.execute(query, (item_id,))
        except Exception as e:
            print(f"Error: {e}")
            raise e

    def _delete_from_discarded_items(self, item_id):
        try:
            query = "DELETE FROM discarded_items WHERE id = %s"
            self.cursor.execute(query, (item_id,))
        except Exception as e:
            print(f"Error: {e}")
            raise e

    def _delete_related_notifications(self, menu_id):
        try:
            query = """
            DELETE nr FROM notification_replies nr
            JOIN notifications n ON nr.notification_id = n.id
            WHERE n.message LIKE %s
            """
            self.cursor.execute(query, (f"%MenuID: {menu_id}%",))
            
            query = "DELETE FROM notifications WHERE message LIKE %s"
            self.cursor.execute(query, (f"%MenuID: {menu_id}%",))
        except Exception as e:
            print(f"Error: {e}")
            raise e

    def delete_item(self, item_id):
        try:
            menu_id = self._get_menu_id(item_id)
            if not menu_id:
                return "Item not found in discarded items."
            
            self._delete_from_discarded_items(item_id)
            self._delete_related_notifications(menu_id)
            
            self.db.commit()
        except Exception as e:
            self.db.rollback()  
            print(f"Error: {e}")
            raise e

    def get_item_name(self, item_id):
        try:
            query = "SELECT name FROM discarded_items WHERE id = %s"
            self.cursor.execute(query, (item_id,))
            result = self.cursor.fetchone()
            if result:
                return result['name']
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def fetch_all_menu_items_with_feedback(self):
        return MenuRepository().fetch_all_menu_items_with_feedback()

    def move_item_to_discard(self, item, avg_rating, sentiment):
        try:
            UtilityRepository().delete_related_entries(item['id'])  
            avg_rating = avg_rating if avg_rating is not None else 0
            sentiment = sentiment if sentiment is not None else 'Neutral'
            insert_query = """
            INSERT INTO discarded_items (menu_id, name, price, availability, spice_level, food_category, dietary_type, average_rating, sentiments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (item['id'], item['name'], item['price'], item['availability'], item['spice_level'], item['food_category'], item['dietary_type'], avg_rating, sentiment))
            delete_query = "DELETE FROM menu WHERE id = %s"
            self.cursor.execute(delete_query, (item['id'],))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Error: {e}")
            raise e
