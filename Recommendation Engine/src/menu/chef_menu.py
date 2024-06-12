import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.feedback_service import FeedbackService
from src.services.report_service import ReportService
from src.services.recommendation_service import RecommendationService

class ChefMenu:
    MENU_CHOICES = {
        'VIEW_FEEDBACK': '1',
        'GENERATE_REPORT': '2',
        'GENERATE_RECOMMENDATIONS': '3',
        'LOGOUT': '4'
    }

    @staticmethod
    def display():
        print("\nChef Menu")
        print("1. View Feedback")
        print("2. Generate Monthly Feedback Report")
        print("3. Generate Recommendations")
        print("4. Logout")

    @staticmethod
    def handle_choice(choice):
        actions = {
            ChefMenu.MENU_CHOICES['VIEW_FEEDBACK']: FeedbackService.view_feedback,
            ChefMenu.MENU_CHOICES['GENERATE_REPORT']: ReportService.generate_report,
            ChefMenu.MENU_CHOICES['GENERATE_RECOMMENDATIONS']: RecommendationService.generate_recommendations,
            ChefMenu.MENU_CHOICES['LOGOUT']: ChefMenu.logout
        }

        action = actions.get(choice, ChefMenu.invalid_choice)
        return action()

    @staticmethod
    def logout():
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True
