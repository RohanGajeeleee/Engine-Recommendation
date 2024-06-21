import mysql.connector
from src.Database.db_config import get_db_connection
from src.models.sentiment_analysis import analyze_sentiment, convert_score_to_sentiment, SentimentAnalyzer
from src.models.notifications import Notification

class Recommendation:
    @staticmethod
    def fetch_available_menu_items():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT id, name FROM menu WHERE availability = TRUE"
            cursor.execute(query)
            items = cursor.fetchall()
            return items
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def recommend_items_for_next_day(threshold=3.0):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = """
            SELECT m.id, m.name, AVG(f.rating) AS avg_rating, COUNT(f.id) AS feedback_count
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            GROUP BY m.id, m.name
            HAVING avg_rating IS NULL OR avg_rating >= %s
            """
            cursor.execute(query, (threshold,))
            results = cursor.fetchall()
            
            cursor.execute("TRUNCATE TABLE recommendations")
            for item in results:
                cursor.execute("INSERT INTO recommendations (menu_id) VALUES (%s)", (item[0],))
            db.commit()

            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def choose_items_for_next_day():
        items = Recommendation.fetch_available_menu_items()
        if not items:
            print("No items available to choose.")
            return

        print("Choose items for the next day:")
        Recommendation.display_items(items)

        chosen_items = Recommendation.get_chosen_items(items)
        if chosen_items:
            Recommendation.update_next_day_menu(chosen_items)
            Notification.send_to_all_employees("Menu items have been chosen for the next day.")
            print("Menu for the next day has been chosen.")
        else:
            print("No items were chosen for the next day.")

    @staticmethod
    def display_items(items):
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}")

    @staticmethod
    def get_chosen_items(items):
        chosen_items = set()
        valid_ids = {item[0] for item in items}
        while True:
            menu_id = input("Enter menu ID to add to the next day's menu (or 'done' to finish): ")
            if menu_id.lower() == 'done':
                if not chosen_items:
                    print("You must select at least one item.")
                    continue
                break
            try:
                menu_id = int(menu_id)
                if menu_id not in valid_ids:
                    print("Invalid menu ID. Please choose a valid menu item.")
                elif menu_id in chosen_items:
                    print("Menu item already selected. Please choose a different menu item.")
                else:
                    chosen_items.add(menu_id)
            except ValueError:
                print("Invalid input. Please enter a valid integer menu ID.")
        return chosen_items

    @staticmethod
    def update_next_day_menu(chosen_items):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("TRUNCATE TABLE next_day_menu")
            for item_id in chosen_items:
                cursor.execute("INSERT INTO next_day_menu (menu_id) VALUES (%s)", (item_id,))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def fetch_recommended_items_from_current_menu():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = """
            SELECT cm.menu_id, m.name, m.price, AVG(f.rating) AS avg_rating
            FROM current_menu cm
            JOIN menu m ON cm.menu_id = m.id
            LEFT JOIN feedback f ON m.id = f.menu_id
            GROUP BY cm.menu_id, m.name, m.price
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_recommendation_data(recommendations):
        return [(item[1], item[2], item[3]) for item in recommendations]

    @staticmethod
    def fetch_all_menu_items():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT m.id, m.name, m.price, m.availability,
                   AVG(f.rating) AS avg_rating, COUNT(f.id) AS feedback_count
            FROM menu m
            LEFT JOIN feedback f ON m.id = f.menu_id
            GROUP BY m.id
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def fetch_sentiments():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT menu_id, comment FROM feedback"
            cursor.execute(query)
            results = cursor.fetchall()
            sentiments = [(menu_id, analyze_sentiment(comment)) for menu_id, comment in results]
            return sentiments
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def determine_recommendations(items, sentiments, threshold=3.0):
        sentiment_dict = {item['id']: 0 for item in items}
        for sentiment in sentiments:
            menu_id = sentiment[0]
            if menu_id not in sentiment_dict:
                sentiment_dict[menu_id] = 0
            sentiment_dict[menu_id] += sentiment[1]

        for item in items:
            item['sentiment_score'] = sentiment_dict.get(item['id'], 0)
            item['sentiment'] = convert_score_to_sentiment(item['sentiment_score'])
            if item['feedback_count'] == 0:
                item['recommended'] = "Yes"
            else:
                item['recommended'] = "Yes" if (item['avg_rating'] or 0) >= threshold else "No"
        
        return items

    @staticmethod
    def fetch_all_menu_items_with_details(threshold=3.0):
        items = Recommendation.fetch_all_menu_items()
        if not items:
            return []

        sentiments = Recommendation.fetch_sentiments()
        detailed_items = Recommendation.determine_recommendations(items, sentiments, threshold)

        return detailed_items

    @staticmethod
    def choose_recommended_item(employee_id, menu_id, time_of_day):
        if Recommendation.has_already_chosen(employee_id, menu_id, time_of_day):
            print("You have already chosen this menu item for today at this time.")
            return

        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO choices (employee_id, menu_id, choice_date, time_of_day) VALUES (%s, %s, CURDATE(), %s)"
            cursor.execute(query, (employee_id, menu_id, time_of_day))
            db.commit()
            print("Choice recorded successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def fetch_recommended_items():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT DISTINCT r.menu_id, m.name FROM recommendations r JOIN menu m ON r.menu_id = m.id"
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def has_already_chosen(employee_id, menu_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM choices WHERE employee_id = %s AND menu_id = %s AND choice_date = CURDATE() AND time_of_day = %s"
            cursor.execute(query, (employee_id, menu_id, time_of_day))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def get_chosen_items(items):
        chosen_items = []
        while True:
            menu_id = input("Enter menu ID to add to the next day's menu (or 'done' to finish): ")
            if menu_id.lower() == 'done':
                if not chosen_items:
                    print("You must select at least one item.")
                    continue
                break
            try:
                menu_id = int(menu_id)
                if menu_id not in [item[0] for item in items]:
                    print("Invalid menu ID. Please choose a valid menu item.")
                else:
                    chosen_items.append(menu_id)
            except ValueError:
                print("Invalid input. Please enter a valid integer menu ID.")
        return chosen_items

    @staticmethod
    def clear_choices_table():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("TRUNCATE TABLE choices")
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def save_chosen_items(chosen_items):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            for item_id in chosen_items:
                cursor.execute("INSERT INTO choices (menu_id) VALUES (%s)", (item_id,))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def update_notifications():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE notifications SET message = 'Menu items have been chosen for the next day.' WHERE message LIKE 'New recommended item%'")
            db.commit()
            Notification.send_to_all_employees("Menu items have been updated for the next day.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def choose_items_again():
        items = Recommendation.fetch_available_menu_items()
        if not items:
            print("No available menu items to choose from.")
            return

        Recommendation.display_menu_items(items)
        chosen_items = Recommendation.get_chosen_items(items)

        Recommendation.clear_choices_table()
        Recommendation.save_chosen_items(chosen_items)
        Recommendation.update_notifications()

        print("Menu for the next day has been chosen.")
    @staticmethod
    def fetch_items_to_discard():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            
            query = """
            SELECT m.id, m.name, AVG(f.rating) as avg_rating
            FROM menu m
            JOIN feedback f ON m.id = f.menu_id
            GROUP BY m.id, m.name
            """
            cursor.execute(query)
            items = cursor.fetchall()

           
            sentiments = SentimentAnalyzer.fetch_sentiments()

            sentiment_dict = {}
            for menu_id, score in sentiments:
                sentiment = convert_score_to_sentiment(score)
                if menu_id not in sentiment_dict:
                    sentiment_dict[menu_id] = {'positive': 0, 'negative': 0, 'neutral': 0}
                sentiment_dict[menu_id][sentiment.lower()] += 1

            items_to_discard = []
            for item in items:
                avg_rating = item['avg_rating']
                menu_id = item['id']
                
                if avg_rating < 2 and sentiment_dict.get(menu_id, {}).get('negative', 0) > 0:
                    item['sentiments'] = f"Positive: {sentiment_dict[menu_id]['positive']}, Negative: {sentiment_dict[menu_id]['negative']}, Neutral: {sentiment_dict[menu_id]['neutral']}"
                    items_to_discard.append(item)

            return items_to_discard
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def move_to_discarded_items(items):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            for item in items:
               
                query = "INSERT INTO discarded_items (menu_id, name, average_rating, sentiments) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (item['id'], item['name'], item['avg_rating'], item['sentiments']))

           
            db.commit()

           
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            for item in items:
               
                query_list = [
                    "DELETE FROM current_menu WHERE menu_id = %s",
                    "DELETE FROM next_day_menu WHERE menu_id = %s",
                    "DELETE FROM choices WHERE menu_id = %s",
                    "DELETE FROM menu WHERE id = %s"
                ]
                for query in query_list:
                    cursor.execute(query, (item['id'],))

            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def fetch_discarded_items():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT menu_id, name, average_rating, sentiments FROM discarded_items"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def remove_item_from_discarded(item_name):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "DELETE FROM discarded_items WHERE name = %s"
            cursor.execute(query, (item_name,))
            db.commit()
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def bring_back_discarded_item(item_name):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            
            query = "SELECT * FROM discarded_items WHERE name = %s"
            cursor.execute(query, (item_name,))
            item = cursor.fetchone()

            if not item:
                print(f"Item '{item_name}' not found in discarded items.")
                return

            query = "INSERT INTO menu (id, name, price, availability) VALUES (%s, %s, %s, 'Available')"
            cursor.execute(query, (item['menu_id'], item['name'], item['average_rating']))  

            query = "DELETE FROM discarded_items WHERE name = %s"
            cursor.execute(query, (item_name,))

            query = "DELETE FROM feedback WHERE menu_id = %s"
            cursor.execute(query, (item['menu_id'],))

            db.commit()
            print(f"Item '{item_name}' has been brought back to the menu and associated feedback has been removed.")
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()