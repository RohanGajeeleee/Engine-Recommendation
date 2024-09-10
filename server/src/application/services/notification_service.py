from src.infrastructure.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self):
        self.notification_repository = NotificationRepository()

    def send_to_all_employees(self, message):
        employees = self.notification_repository.get_all_employee_ids()
        for employee_id in employees:
            self.notification_repository.add_notification(employee_id, message)

    def send_to_employee(self, employee_id, message):
        self.notification_repository.add_notification(employee_id, message)

    def view_notifications(self, employee_id):
        notifications = self.notification_repository.get_notifications_for_employee(employee_id)
        if not notifications:
            return "No new notifications."
        
        response = "\nNotifications:\n"
        for notification in notifications:
            response += f"- {notification['message']} (Received at: {notification['created_at']})\n"
            self.notification_repository.mark_as_read(notification['id'])
        
        return response

    def send_new_menu_notification(self, menu_items):
        message = "New menu for the next day:\n"
        for item in menu_items:
            message += f"- {item['name']} (ID: {item['id']})\n"
        self.send_to_all_employees(message)
