import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.services.feedback_service import FeedbackService
from src.services.employee_service import EmployeeService
from src.services.recommendation_service import RecommendationService
from src.services.notification_service import NotificationService

class EmployeeMenu:
    MENU_CHOICES = {
        'ADD_FEEDBACK': '1',
        'VIEW_FEEDBACK': '2',
        'CHOOSE_RECOMMENDED_ITEM': '3',
        'VIEW_NOTIFICATIONS': '4',
        'LOGOUT': '5'
    }

    @staticmethod
    def display():
        print("\nEmployee Menu")
        print("1. Add Feedback")
        print("2. View Feedback")
        print("3. Choose Recommended Item")
        print("4. View Notifications")
        print("5. Logout")

    @staticmethod
    def handle_choice(employee_id, choice, first_day, current_date):
        if first_day and choice == EmployeeMenu.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']:
            print("Menu will be ready tomorrow.")
            return True

        actions = {
            EmployeeMenu.MENU_CHOICES['ADD_FEEDBACK']: lambda: FeedbackService.add_feedback(employee_id,current_date),
            EmployeeMenu.MENU_CHOICES['VIEW_FEEDBACK']: FeedbackService.view_feedback,
            EmployeeMenu.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']: lambda: RecommendationService.choose_recommended_item(employee_id),
            EmployeeMenu.MENU_CHOICES['VIEW_NOTIFICATIONS']: lambda: NotificationService.view_notifications(employee_id),
            EmployeeMenu.MENU_CHOICES['LOGOUT']: EmployeeMenu.logout
        }

        action = actions.get(choice, EmployeeMenu.invalid_choice)
        result = action()
        return result

    @staticmethod
    def logout():
        return False

    @staticmethod
    def invalid_choice():
        print("Invalid choice. Please try again.")
        return True
