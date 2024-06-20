import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.services.feedback_service import FeedbackService
from src.services.recommendation_service import RecommendationService
from src.services.notification_service import NotificationService
from src.models.user import User

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
        actions = {
            EmployeeMenu.MENU_CHOICES['ADD_FEEDBACK']: lambda: EmployeeMenu.add_feedback(employee_id, current_date),
            EmployeeMenu.MENU_CHOICES['VIEW_FEEDBACK']: lambda: EmployeeMenu.view_feedback(employee_id),
            EmployeeMenu.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']: lambda: EmployeeMenu.choose_recommended_item(employee_id),
            EmployeeMenu.MENU_CHOICES['VIEW_NOTIFICATIONS']: lambda: EmployeeMenu.view_notifications(employee_id),
            EmployeeMenu.MENU_CHOICES['LOGOUT']: lambda: EmployeeMenu.logout(employee_id)
        }

        action = actions.get(choice, lambda: EmployeeMenu.invalid_choice(employee_id))
        result = action()
        return result

    @staticmethod
    def add_feedback(employee_id, current_date):
        FeedbackService.add_feedback(employee_id, current_date)
        User.log_activity(employee_id, 'add_feedback', 'Added feedback')
        return True

    @staticmethod
    def view_feedback(employee_id):
        FeedbackService.view_feedback()
        User.log_activity(employee_id, 'view_feedback', 'Viewed feedback')
        return True

    @staticmethod
    def choose_recommended_item(employee_id):
        RecommendationService.choose_recommended_item(employee_id)
        User.log_activity(employee_id, 'choose_recommended_item', 'Chose recommended item')
        return True

    @staticmethod
    def view_notifications(employee_id):
        NotificationService.view_notifications(employee_id)
        User.log_activity(employee_id, 'view_notifications', 'Viewed notifications')
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
