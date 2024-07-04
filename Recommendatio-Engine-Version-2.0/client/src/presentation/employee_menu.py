import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.presentation.profile_manager import ProfileManager
from src.presentation.feedback_manager import FeedbackManager
from src.presentation.recommendation_manager import RecommendationManager
from src.presentation.notification_manager import NotificationManager
from src.presentation.feedback_request_manager import FeedbackRequestManager


class EmployeeMenu:
    MENU_CHOICES = {
        'ADD_FEEDBACK': '1',
        'VIEW_FEEDBACK': '2',
        'CHOOSE_RECOMMENDED_ITEM': '3',
        'VIEW_NOTIFICATIONS': '4',
        'REPLY_FEEDBACK_REQUEST': '5',
        'UPDATE_PROFILE': '6',
        'LOGOUT': '7'
    }

    def __init__(self):
        self.feedback_manager = FeedbackManager()
        self.recommendation_manager = RecommendationManager()
        self.notification_manager = NotificationManager()
        self.feedback_request_manager = FeedbackRequestManager()
        self.profile_manager = ProfileManager()

    def display(self):
        print("\nEmployee Menu")
        print("1. Add Feedback")
        print("2. View Feedback")
        print("3. Choose Recommended Item")
        print("4. View Notifications")
        print("5. Reply to Feedback Request")
        print("6. Update Profile")
        print("7. Logout")
    
    def handle_choice(self, employee_id, choice, first_day, current_date):
        actions = {
            self.MENU_CHOICES['ADD_FEEDBACK']: lambda: self.feedback_manager.add_feedback(employee_id, current_date),
            self.MENU_CHOICES['VIEW_FEEDBACK']: self.feedback_manager.view_feedback,
            self.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']: lambda: self.recommendation_manager.choose_recommended_item(employee_id),
            self.MENU_CHOICES['VIEW_NOTIFICATIONS']: lambda: self.notification_manager.view_notifications(employee_id),
            self.MENU_CHOICES['REPLY_FEEDBACK_REQUEST']: lambda: self.feedback_request_manager.reply_to_request(employee_id),
            self.MENU_CHOICES['UPDATE_PROFILE']: lambda: self.profile_manager.update_profile(employee_id),
            self.MENU_CHOICES['LOGOUT']: self.logout
        }
        action = actions.get(choice, self.invalid_choice)
        return action()

    def logout(self):
        print("Logged out successfully")
        return False

    def invalid_choice(self):
        print("Invalid choice. Please try again.")
        return True
