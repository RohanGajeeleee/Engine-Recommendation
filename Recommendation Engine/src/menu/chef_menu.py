import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.models.feedback import Feedback
from src.models.reporting import Report
from src.services.recommendation_service import RecommendationService

class ChefMenu:
    MENU_CHOICES = {
        'VIEW_FEEDBACK': '1',
        'GENERATE_REPORT': '2',
        'CHOOSE_ITEMS_FOR_NEXT_DAY': '3',
        'GENERATE_RECOMMENDATIONS': '4',
        'LOGOUT': '5'
    }

    @staticmethod
    def display():
        print("\nChef Menu")
        print("1. View Feedback")
        print("2. Generate Monthly Feedback Report")
        print("3. Choose Items for Next Day")
        print("4. Generate Recommendations")
        print("5. Logout")

    @staticmethod
    def handle_choice(choice):
        actions = {
            ChefMenu.MENU_CHOICES['VIEW_FEEDBACK']: ChefMenu.view_feedback,
            ChefMenu.MENU_CHOICES['GENERATE_REPORT']: ChefMenu.generate_report,
            ChefMenu.MENU_CHOICES['CHOOSE_ITEMS_FOR_NEXT_DAY']: ChefMenu.choose_items_for_next_day,
            ChefMenu.MENU_CHOICES['GENERATE_RECOMMENDATIONS']: ChefMenu.generate_recommendations,
            ChefMenu.MENU_CHOICES['LOGOUT']: ChefMenu.logout
        }

        action = actions.get(choice, ChefMenu.invalid_choice)
        return action()

    @staticmethod
    def view_feedback():
        Feedback.view()
        return True

    @staticmethod
    @staticmethod
    def generate_report():
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
        return True
    
    @staticmethod
    def choose_items_for_next_day():
        RecommendationService.choose_items_for_next_day()
        return True

    @staticmethod
    def generate_recommendations():
        RecommendationService.list_all_menu_items()
        return True

    @staticmethod
    def logout():
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True
