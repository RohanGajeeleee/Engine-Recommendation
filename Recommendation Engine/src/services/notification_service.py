from src.models.notifications import Notification

class NotificationService:
    @staticmethod
    def view_notifications(employee_id):
        notifications = Notification.fetch_and_clear_notifications(employee_id)
        if notifications:
            print("Notifications:")
            for notification in notifications:
                print(f"Message: {notification['message']}")
        else:
            print("No new notifications.")
        return True
