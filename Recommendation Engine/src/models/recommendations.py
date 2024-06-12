import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# src/recommendation.py

import mysql.connector
from src.Database.db_config import get_db_connection
from src.models.sentiment_analysis import analyze_sentiment
from src.models.notifications import Notification

class Recommendation:
    @staticmethod
    def fetch_available_menu_items():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT id, name FROM menu WHERE availability is true"
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
            
            # Insert recommendations into the recommendations table
            cursor.execute("TRUNCATE TABLE recommendations")
            for item in results:
                cursor.execute("INSERT INTO recommendations (menu_id) VALUES (%s)", (item[0],))
            db.commit()

            # Send a single notification to all employees
            Notification.send_to_all_employees("New recommendation menu available.")

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
    def analyze_feedback_comments():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT menu_id, comment FROM feedback"
            cursor.execute(query)
            results = cursor.fetchall()
            sentiments = []
            for menu_id, comment in results:
                sentiment = analyze_sentiment(comment)
                sentiments.append((menu_id, comment, sentiment))
            return sentiments
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def choose_recommended_item(employee_id, menu_id):
        if Recommendation.has_already_chosen(employee_id):
            print("You have already chosen a menu item for today.")
            return

        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO choices (employee_id, menu_id, choice_date) VALUES (%s, %s, CURDATE())"
            cursor.execute(query, (employee_id, menu_id))
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
    def has_already_chosen(employee_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM choices WHERE employee_id = %s AND choice_date = CURDATE()"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
