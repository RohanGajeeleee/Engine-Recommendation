from src.models.recommendations import Recommendation
from src.models.notifications import Notification
import mysql.connector
from src.Database.db_config import get_db_connection

class RecommendationService:
    @staticmethod
    def list_all_menu_items():
        items = Recommendation.fetch_all_menu_items_with_details()
        if items:
            print("\nComplete Menu:")
            for item in items:
                avg_rating = "No Rating" if item['avg_rating'] is None or item['avg_rating'] == 0 else f"{item['avg_rating']:.2f}"
                feedback_count = item['feedback_count'] if item['feedback_count'] is not None else 0
                sentiment = item['sentiment']
                recommended = item['recommended']
                print(f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']},  Average Rating: {avg_rating}, Feedback Count: {feedback_count}, Sentiment: {sentiment}, Recommended: {recommended}")
        else:
            print("No menu items available.")

    @staticmethod
    def generate_recommendations():
        recommendations = Recommendation.recommend_items_for_next_day()
        RecommendationService.list_all_menu_items()
        return recommendations
    
    @staticmethod
    def choose_items_for_next_day():
        Recommendation.choose_items_for_next_day()
        return True

    @staticmethod
    def choose_recommended_item(employee_id):
        recommended_items = Recommendation.fetch_recommended_items_from_current_menu()
        if recommended_items:
            print("Recommended Items for Next Day:")
            for item in recommended_items:
                avg_rating = "No Rating yet" if item[3] is None or item[3] == 0 else f"{item[3]:.2f}"
                print(f"ID: {item[0]}, Name: {item[1]}, Price: {item[2]}, Average Rating: {avg_rating}")
            while True:
                try:
                    menu_id = int(input("Enter recommended menu ID to choose: "))
                    if menu_id not in [item[0] for item in recommended_items]:
                        print("Invalid menu ID. Please choose a valid recommended item.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid integer menu ID.")

            time_of_day = input("Enter time of day (1.breakfast, 2.lunch, 3.dinner): ").lower()
            if time_of_day not in ['1', '2', '3']:
                print("Invalid time of day. Please choose '1 for breakfast', '2 for lunch', or '3 for dinner'.")
            else:
                Recommendation.choose_recommended_item(employee_id, menu_id, time_of_day)
        else:
            print("No recommended items available.")
        return True

    @staticmethod
    def confirm_menu_for_next_day():
        RecommendationService.generate_recommendations()
        chosen_items = []
        while True:
            menu_id = input("Enter menu ID to confirm (or 'done' to finish): ")
            if menu_id.lower() == 'done':
                if not chosen_items:
                    print("You must select at least one item.")
                    continue
                break
            try:
                menu_id = int(menu_id)
                chosen_items.append(menu_id)
            except ValueError:
                print("Invalid input. Please enter a valid integer menu ID.")
        
        Recommendation.confirm_menu_for_next_day(chosen_items)
        print("Menu for the next day has been confirmed.")
        return True

    @staticmethod
    def generate_custom_recommendations():
        try:
            num_items = int(input("How many items would you like to display? "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        detailed_items = Recommendation.fetch_all_menu_items_with_details()
        recommended_items = [item for item in detailed_items if item['recommended'] == "Yes"]


        if len(recommended_items) >= num_items:
            items_to_display = recommended_items[:num_items]
        else:
            items_to_display = recommended_items
            print(f"Only {len(items_to_display)} recommended items available to display.")

           
        print("Custom Recommendations:")
        for item in items_to_display:
            avg_rating = "No Rating" if item['avg_rating'] is None or item['avg_rating'] == 0 else f"{item['avg_rating']:.2f}"
            print(f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Average Rating: {avg_rating}, Recommended: {item['recommended']}")
    @staticmethod
    def check_discard_criteria():
        items_to_discard = Recommendation.fetch_items_to_discard()
        if items_to_discard:
            Recommendation.move_to_discarded_items(items_to_discard)
    @staticmethod
    def get_discarded_items():
        return Recommendation.fetch_discarded_items()

    @staticmethod
    def remove_item(item_name):
        Recommendation.remove_item_from_discarded(item_name)
        print(f"Item '{item_name}' removed from menu.")

    @staticmethod
    def request_detailed_feedback(item_name):
        Notification.send_to_all_employees(
            f"We are trying to improve your experience with {item_name}. Please provide your feedback and help us. "
            f"Q1. What didn’t you like about {item_name}? "
            f"Q2. How would you like {item_name} to taste? "
            f"Q3. Share your mom’s recipe"
        )
        print(f"Feedback request sent for '{item_name}'.")
        
    @staticmethod
    def check_discard_criteria():
        items_to_discard = Recommendation.fetch_items_to_discard()
        if items_to_discard:
            Recommendation.move_to_discarded_items(items_to_discard)
    @staticmethod
    def bring_back_discarded_item(item_name):
        Recommendation.bring_back_discarded_item(item_name)
        print(f"Item '{item_name}' has been brought back to the menu.")
    @staticmethod
    def send_detailed_feedback_to_chef(employee_id, item_id, feedback):
        feedback_message = (
            f"Detailed Feedback for Item ID {item_id} from Employee ID {employee_id}\n"
            f"Q1: {feedback['Q1']}\n"
            f"Q2: {feedback['Q2']}\n"
            f"Q3: {feedback['Q3']}\n"
        )
        Notification.send_to_chef(feedback_message)

    @staticmethod
    def get_discarded_items():
        return Recommendation.fetch_discarded_items()

    @staticmethod
    def remove_item(item_name):
        Recommendation.remove_item_from_discarded(item_name)
        print(f"Item '{item_name}' removed from menu.")

    @staticmethod
    def request_detailed_feedback(item_name):
        message = (
            f"We are trying to improve your experience with {item_name}. Please provide your feedback and help us.\n"
            f"Q1. What didn’t you like about {item_name}?\n"
            f"Q2. How would you like {item_name} to taste?\n"
            f"Q3. Share your mom’s recipe for {item_name}."
        )
        Notification.send_to_all_employees(message)
        print(f"Feedback request sent for '{item_name}'.")

    @staticmethod
    def check_discard_criteria():
        items_to_discard = Recommendation.fetch_items_to_discard()
        if items_to_discard:
            Recommendation.move_to_discarded_items(items_to_discard)
    @staticmethod
    def prompt_detailed_feedback(item_id):
        feedback = {}
        feedback['Q1'] = input(f"Q1. What didn’t you like about item ID {item_id}? ")
        feedback['Q2'] = input(f"Q2. How would you like item ID {item_id} to taste? ")
        feedback['Q3'] = input(f"Q3. Share your mom’s recipe for item ID {item_id}. ")
        return feedback

    @staticmethod
    def get_feedback_replies():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT r.employee_id, r.reply, r.reply_date
            FROM notification_replies r
            JOIN notifications n ON r.notification_id = n.id
            WHERE n.message LIKE 'We are trying to improve your experience with%' 
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()