import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.services.feedback_service import FeedbackService
from src.services.recommendation_service import RecommendationService
from src.services.notification_service import NotificationService
from src.models.notifications import NotificationDatabaseHandler
from src.models.user import User

class EmployeeMenu:
    MENU_CHOICES = {
        'ADD_FEEDBACK': '1',
        'VIEW_FEEDBACK': '2',
        'CHOOSE_RECOMMENDED_ITEM': '3',
        'VIEW_NOTIFICATIONS': '4',
        'REPLY_TO_FEEDBACK_REQUEST': '5',  # New option
        'LOGOUT': '6'
    }

    @staticmethod
    def display():
        print("\nEmployee Menu")
        print("1. Add Feedback")
        print("2. View Feedback")
        print("3. Choose Recommended Item")
        print("4. View Notifications")
        print("5. Reply to Feedback Request")  # New option
        print("6. Logout")

    @staticmethod
    def handle_choice(employee_id, choice, first_day, current_date):
        actions = {
            EmployeeMenu.MENU_CHOICES['ADD_FEEDBACK']: lambda: EmployeeMenu.add_feedback(employee_id, current_date),
            EmployeeMenu.MENU_CHOICES['VIEW_FEEDBACK']: lambda: EmployeeMenu.view_feedback(employee_id),
            EmployeeMenu.MENU_CHOICES['CHOOSE_RECOMMENDED_ITEM']: lambda: EmployeeMenu.choose_recommended_item(employee_id),
            EmployeeMenu.MENU_CHOICES['VIEW_NOTIFICATIONS']: lambda: EmployeeMenu.view_notifications(employee_id),
            EmployeeMenu.MENU_CHOICES['REPLY_TO_FEEDBACK_REQUEST']: lambda: EmployeeMenu.reply_to_feedback_request(employee_id),  # New option
            EmployeeMenu.MENU_CHOICES['LOGOUT']: lambda: EmployeeMenu.logout(employee_id)
        }

        action = actions.get(choice, lambda: EmployeeMenu.invalid_choice(employee_id))
        result = action()
        return result

    @staticmethod
    def reply_to_feedback_request(employee_id):
        notifications = NotificationDatabaseHandler.get_feedback_request_notifications()
        if not notifications:
            print("No feedback requests found.")
            return True

        print("Feedback Requests for Discarded Items:")
        for notification in notifications:
            print(f"Notification ID: {notification['id']}, Message: {notification['message']}")

        notification_id = int(input("Enter the Notification ID to reply to: "))
        notification = next((n for n in notifications if n['id'] == notification_id), None)
        if not notification:
            print("Invalid Notification ID.")
            return True

        item_name = notification['message'].split(' ')[5]  # Assuming the item name is at the 5th position in the message
        reply1 = input(f"Q1. What didn’t you like about {item_name}? ")
        reply2 = input(f"Q2. How would you like {item_name} to taste? ")
        reply3 = input(f"Q3. Share your mom’s recipe for {item_name}. ")

        complete_reply = f"Q1. {reply1}\nQ2. {reply2}\nQ3. {reply3}"

        NotificationDatabaseHandler.save_reply(notification_id, employee_id, complete_reply)
        print(f"Reply sent for '{item_name}'.")
        return True

    @staticmethod
    def reply_to_discard_item(employee_id):
        discarded_items = RecommendationService.get_discarded_items()
        if not discarded_items:
            print("No discarded items requiring feedback.")
            return True

        for item in discarded_items:
            print(f"Discarded Item ID: {item['menu_id']}, Name: {item['name']}")

        while True:
            try:
                item_id = int(input("Enter the Discarded Item ID to reply to: ").strip())
                if item_id not in [item['menu_id'] for item in discarded_items]:
                    print("Invalid Item ID. Please try again.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid Item ID.")

        feedback = EmployeeMenu.prompt_detailed_feedback(item_id)
        RecommendationService.send_detailed_feedback_to_chef(employee_id, item_id, feedback)
        return True

    @staticmethod
    def prompt_detailed_feedback(item_id):
        feedback = {}
        feedback['Q1'] = input(f"Q1. What didn’t you like about item ID {item_id}? ")
        feedback['Q2'] = input(f"Q2. How would you like item ID {item_id} to taste? ")
        feedback['Q3'] = input(f"Q3. Share your mom’s recipe for item ID {item_id}. ")
        return feedback

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
