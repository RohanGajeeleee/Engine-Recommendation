import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.models.feedback import Feedback
from src.models.reporting import Report
from src.services.recommendation_service import RecommendationService
from src.models.user import User

class ChefMenu:
    MENU_CHOICES = {
        'VIEW_FEEDBACK': '1',
        'GENERATE_REPORT': '2',
        'CHOOSE_ITEMS_FOR_NEXT_DAY': '3',
        'GENERATE_CUSTOM_RECOMMENDATIONS': '4',
        'VIEW_DISCARD_LIST': '5',
        'VIEW_FEEDBACK_REPLIES': '6',  
        'LOGOUT': '7'
    }

    @staticmethod
    def display():
        print("\nChef Menu")
        print("1. View Feedback")
        print("2. Generate Monthly Feedback Report")
        print("3. Choose Items for Next Day")
        print("4. Generate Custom Recommendations")
        print("5. View Discard Menu Item List")
        print("6. View Feedback Replies")  
        print("7. Logout")

    @staticmethod
    def handle_choice(choice, employee_id):
        actions = {
            ChefMenu.MENU_CHOICES['VIEW_FEEDBACK']: lambda: ChefMenu.view_feedback(employee_id),
            ChefMenu.MENU_CHOICES['GENERATE_REPORT']: lambda: ChefMenu.generate_report(employee_id),
            ChefMenu.MENU_CHOICES['CHOOSE_ITEMS_FOR_NEXT_DAY']: lambda: ChefMenu.choose_items_for_next_day(employee_id),
            ChefMenu.MENU_CHOICES['GENERATE_CUSTOM_RECOMMENDATIONS']: ChefMenu.generate_custom_recommendations,
            ChefMenu.MENU_CHOICES['VIEW_DISCARD_LIST']: lambda: ChefMenu.view_discard_list(employee_id),
            ChefMenu.MENU_CHOICES['VIEW_FEEDBACK_REPLIES']: lambda: ChefMenu.view_feedback_replies(employee_id),  
            ChefMenu.MENU_CHOICES['LOGOUT']: lambda: ChefMenu.logout(employee_id)
        }

        action = actions.get(choice, lambda: ChefMenu.invalid_choice(employee_id))
        return action()

    @staticmethod
    def view_feedback_replies(employee_id):
        replies = RecommendationService.get_feedback_replies()
        if replies:
            for reply in replies:
                print(f"Employee ID: {reply['employee_id']}, Reply: {reply['reply']}, Date: {reply['reply_date']}")
        else:
            print("No feedback replies available.")
        return True
    @staticmethod
    def view_discard_list(employee_id):
        discarded_items = RecommendationService.get_discarded_items()
        if discarded_items:
            for item in discarded_items:
                print(f"Food Item: {item['name']}, Average Rating: {item['average_rating']}, Sentiments: {item['sentiments']}")
            while True:
                choice = input("Enter 1 to Remove Item, 2 to Get Detailed Feedback, 3 to Bring Back Item, or 'done' to finish: ").strip()
                if choice == 'done':
                    return True
                elif choice == '1':
                    item_name = input("Enter the Food Item name to remove: ").strip()
                    RecommendationService.remove_item(item_name)
                    return True
                elif choice == '2':
                    item_name = input("Enter the Food Item name to get detailed feedback: ").strip()
                    RecommendationService.request_detailed_feedback(item_name)
                elif choice == '3':
                    item_name = input("Enter the Food Item name to bring back to the menu: ").strip()
                    RecommendationService.bring_back_discarded_item(item_name)
                    return True
                else:
                    print("Invalid choice. Please enter 1, 2, 3, or 'done'.")
        else:
            print("No items to discard.")
            return True
            
    @staticmethod
    def view_feedback(employee_id):
        Feedback.view()
        User.log_activity(employee_id, 'view_feedback', 'Viewed feedback')
        return True

    @staticmethod
    def generate_report(employee_id):
        while True:
            try:
                year = int(input("Enter year: ").strip())
                if year < 1900 or year > 2100:
                    print("Invalid year. Please enter a year between 1900 and 2100.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid year.")

        while True:
            try:
                month = int(input("Enter month (1-12): ").strip())
                if month < 1 or month > 12:
                    print("Invalid month. Please enter a month between 1 and 12.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a valid month.")

        Report.generate_monthly_feedback_report(year, month)
        User.log_activity(employee_id, 'generate_report', 'Generated monthly feedback report')
        return True
    
    @staticmethod
    def choose_items_for_next_day(employee_id):
        RecommendationService.choose_items_for_next_day()
        User.log_activity(employee_id, 'choose_items_for_next_day', 'Chose items for the next day')
        return True
    
    @staticmethod
    def generate_custom_recommendations():
        RecommendationService.generate_custom_recommendations()
        return True

    @staticmethod
    def logout(employee_id):
        User.log_activity(employee_id, 'logout', 'User logged out')
        return False

    @staticmethod
    def invalid_choice(employee_id):
        print("Invalid choice. Please try again.")
        User.log_activity(employee_id, 'invalid_choice', 'Invalid menu choice')
        return True
