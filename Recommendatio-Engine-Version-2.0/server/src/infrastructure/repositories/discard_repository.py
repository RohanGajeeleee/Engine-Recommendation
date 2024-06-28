from src.infrastructure.db_config import get_db_connection
from src.infrastructure.repositories.menu_repository import MenuRepository
from src.infrastructure.repositories.utility_repository import UtilityRepository

class DiscardRepository:
    @staticmethod
    def item_exists_in_discard(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM discarded_items WHERE id = %s"
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            return result[0] > 0
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def get_discarded_items():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT id, name, price, availability FROM discarded_items"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def restore_item(item_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            menu_id = DiscardRepository._get_menu_id(cursor, item_id)
            if not menu_id:
                return "Item not found in discarded items."
            
            DiscardRepository._insert_into_menu(cursor, item_id)
            DiscardRepository._delete_from_discarded_items(cursor, item_id)
            DiscardRepository._delete_related_notifications(cursor, menu_id)
            
            db.commit()
        except Exception as e:
            db.rollback() 
            raise e
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def _get_menu_id(cursor, item_id):
        query = "SELECT menu_id FROM discarded_items WHERE id = %s"
        cursor.execute(query, (item_id,))
        result = cursor.fetchone()
        return result['menu_id'] if result else None

    @staticmethod
    def _insert_into_menu(cursor, item_id):
        query = """
        INSERT INTO menu (name, price, availability, spice_level, food_category, dietary_type) 
        SELECT name, price, availability, spice_level, food_category, dietary_type FROM discarded_items WHERE id = %s
        """
        cursor.execute(query, (item_id,))

    @staticmethod
    def _delete_from_discarded_items(cursor, item_id):
        query = "DELETE FROM discarded_items WHERE id = %s"
        cursor.execute(query, (item_id,))

    @staticmethod
    def _delete_related_notifications(cursor, menu_id):
        query = """
        DELETE nr FROM notification_replies nr
        JOIN notifications n ON nr.notification_id = n.id
        WHERE n.message LIKE %s
        """
        cursor.execute(query, (f"%MenuID: {menu_id}%",))
        
        query = "DELETE FROM notifications WHERE message LIKE %s"
        cursor.execute(query, (f"%MenuID: {menu_id}%",))


    @staticmethod
    def delete_item(item_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            menu_id = DiscardRepository._get_menu_id(cursor, item_id)
            if not menu_id:
                return "Item not found in discarded items."
            
            DiscardRepository._delete_from_discarded_items(cursor, item_id)
            DiscardRepository._delete_related_notifications(cursor, menu_id)
            
            db.commit()
        except Exception as e:
            db.rollback()  
            raise e
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_item_name(item_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT name FROM discarded_items WHERE id = %s"
            cursor.execute(query, (item_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        finally:
            cursor.close()
            db.close()
            
    @staticmethod
    def fetch_all_menu_items_with_feedback():
        return MenuRepository.fetch_all_menu_items_with_feedback()

    @staticmethod
    def move_item_to_discard(item, avg_rating, sentiment):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            UtilityRepository.delete_related_entries(item['id'], cursor)
            avg_rating = avg_rating if avg_rating is not None else 0
            sentiment = sentiment if sentiment is not None else 'Neutral'
            insert_query = """
            INSERT INTO discarded_items (menu_id, name, price, availability, spice_level, food_category, dietary_type, average_rating, sentiments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (item['id'], item['name'], item['price'], item['availability'], item['spice_level'], item['food_category'], item['dietary_type'], avg_rating, sentiment))
            delete_query = "DELETE FROM menu WHERE id = %s"
            cursor.execute(delete_query, (item['id'],))
            db.commit()
        finally:
            cursor.close()
            db.close()