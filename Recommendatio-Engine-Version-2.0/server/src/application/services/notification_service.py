from src.infrastructure.repositories.notification_repository import NotificationRepository

class NotificationService:
    @staticmethod
    def send_to_all_employees(message):
        employees = NotificationRepository.get_all_employee_ids()
        for employee_id in employees:
            NotificationRepository.add_notification(employee_id, message)

    @staticmethod
    def send_to_employee(employee_id, message):
        NotificationRepository.add_notification(employee_id, message)
    @staticmethod
    def view_notifications(employee_id):
        notifications = NotificationRepository.get_notifications_for_employee(employee_id)
        if not notifications:
            return "No new notifications."
        
        response = "\nNotifications:\n"
        for notification in notifications:
            response += f"- {notification['message']} (Received at: {notification['created_at']})\n"
            NotificationRepository.mark_as_read(notification['id'])
        
        return response
    @staticmethod
    def send_new_menu_notification(menu_items):
        message = "New menu for the next day:\n"
        for item in menu_items:
            message += f"- {item['name']} (ID: {item['id']})\n"
        NotificationService.send_to_all_employees(message)
