import mysql.connector
from src.Database.db_config import get_db_connection
from src.models.sentiment_analysis import analyze_sentiment

class DiscardService:
    @staticmethod
    def identify_and_remove_items_to_discard():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT m.id, m.name, AVG(f.rating) AS avg_rating
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            GROUP BY m.id, m.name
            HAVING AVG(f.rating) < 2
            """
            cursor.execute(query)
            low_rating_items = cursor.fetchall()

            for item in low_rating_items:
                item_id = item['id']
                query = "SELECT comment FROM feedback WHERE menu_id = %s"
                cursor.execute(query, (item_id,))
                comments = cursor.fetchall()
                negative_sentiments = sum(analyze_sentiment(comment['comment']) < 0 for comment in comments)

                if negative_sentiments > 0:
                    DiscardService.remove_item_from_all_tables(item_id)
                    DiscardService.add_item_to_discard_list(item_id, item['name'], item['avg_rating'], comments)

            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def remove_item_from_all_tables(menu_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            tables = ["choices", "current_menu", "next_day_menu", "recommendations"]
            for table in tables:
                query = f"DELETE FROM {table} WHERE menu_id = %s"
                cursor.execute(query, (menu_id,))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def add_item_to_discard_list(menu_id, name, avg_rating, comments):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            sentiments = ", ".join(comment['comment'] for comment in comments)
            query = "INSERT INTO discarded_items (menu_id, average_rating, sentiments) VALUES (%s, %s, %s)"
            cursor.execute(query, (menu_id, avg_rating, sentiments))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
