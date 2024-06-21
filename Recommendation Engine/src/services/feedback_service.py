import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.Database.db_config import get_db_connection
from src.models.feedback import Feedback
import mysql.connector


class FeedbackService:
    @staticmethod
    def view_feedback():
        Feedback.view()
        return True

    @staticmethod
    def add_feedback(employee_id, current_date):
        choices = ChoiceFetcher.fetch_choices(employee_id)
        if not choices:
            print("No items available for feedback.")
            return True

        ChoiceDisplayer.display_choices(choices)
        menu_id, time_of_day = InputHandler.get_menu_id_and_time_of_day(choices)
        comment = InputHandler.get_comment()
        rating = InputHandler.get_rating()

        feedback = Feedback(employee_id, menu_id, comment, rating)
        feedback.add(current_date)

        FeedbackMarker.mark_feedback_given(employee_id, menu_id, time_of_day)
        return True


class ChoiceFetcher:
    @staticmethod
    def fetch_choices(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT c.menu_id, m.name, c.time_of_day
            FROM choices c 
            JOIN menu m ON c.menu_id = m.id 
            WHERE c.employee_id = %s AND c.feedback_given = 0
            """
            cursor.execute(query, (employee_id,))
            choices = cursor.fetchall()
            return choices
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()


class ChoiceDisplayer:
    @staticmethod
    def display_choices(choices):
        print("Items available for feedback:")
        for choice in choices:
            print(f"ID: {choice['menu_id']}, Name: {choice['name']}, Time of Day: {choice['time_of_day']}")


class InputHandler:
    @staticmethod
    def get_menu_id_and_time_of_day(choices):
        time_of_day_map = {'1': 'breakfast', '2': 'lunch', '3': 'dinner'}
        while True:
            menu_id_str = input("Enter menu ID to give feedback: ")
            time_of_day_choice = input("Enter time of day (1: breakfast, 2: lunch, 3: dinner): ").lower()
            time_of_day = time_of_day_map.get(time_of_day_choice)
            if time_of_day is None:
                print("Invalid time of day choice. Please enter 1, 2, or 3.")
                continue
            try:
                menu_id = int(menu_id_str)
                if menu_id not in [choice['menu_id'] for choice in choices if choice['time_of_day'] == time_of_day]:
                    print("Invalid menu ID or time of day. Please choose a valid menu item and time of day.")
                else:
                    return menu_id, time_of_day
            except ValueError:
                print("Invalid input. Please enter a valid integer menu ID.")

    @staticmethod
    def get_comment():
        return input("Enter comment: ")

    @staticmethod
    def get_rating():
        while True:
            rating_str = input("Enter rating (1-5): ")
            try:
                rating = int(rating_str)
                if 1 <= rating <= 5:
                    return rating
                else:
                    print("Invalid rating. Please enter a rating between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a valid integer rating between 1 and 5.")


class FeedbackMarker:
    @staticmethod
    def mark_feedback_given(employee_id, menu_id, time_of_day):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "UPDATE choices SET feedback_given = 1 WHERE employee_id = %s AND menu_id = %s AND time_of_day = %s"
            cursor.execute(query, (employee_id, menu_id, time_of_day))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
