import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import socket
import threading
import mysql.connector
from src.Database.db_config import get_db_connection

class Notification:
    def __init__(self, employee_id=None, message=None):
        self.employee_id = employee_id
        self.message = message

    def save(self):
        """Save a notification to the database."""
        NotificationDatabaseHandler.save_notification(self.employee_id, self.message)

    @staticmethod
    def send(employee_id, message):
        """Send a notification to the specified employee."""
        NotificationSender.send_notification(employee_id, message)

    @staticmethod
    def send_to_all_employees(message):
        """Send a notification to all employees."""
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT employee_id FROM users WHERE role = 'employee'"
            cursor.execute(query)
            employees = cursor.fetchall()
            for employee in employees:
                Notification.send(employee[0], message)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def handle_client(client_socket):
        """Handle incoming client connections."""
        NotificationReceiver.handle_client_connection(client_socket)

    @staticmethod
    def start_server():
        """Start the notification server."""
        NotificationReceiver.start_server()

    @staticmethod
    def fetch_and_clear_notifications(employee_id):
        """Fetch and clear notifications for a user."""
        notifications = NotificationDatabaseHandler.fetch_notifications(employee_id)
        NotificationDatabaseHandler.clear_notifications(employee_id)
        return notifications

class NotificationDatabaseHandler:
    @staticmethod
    def save_notification(employee_id, message):
        """Save a notification to the database."""
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "INSERT INTO notifications (employee_id, message) VALUES (%s, %s)"
            cursor.execute(query, (employee_id, message))
            db.commit()
            print("Notification saved successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def fetch_notifications(employee_id):
        """Fetch notifications for a user."""
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT message, created_at FROM notifications WHERE employee_id = %s AND is_read = 0"
            cursor.execute(query, (employee_id,))
            notifications = cursor.fetchall()
            return notifications
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def clear_notifications(employee_id):
        """Clear notifications for a user."""
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "UPDATE notifications SET is_read = 1 WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

class NotificationSender:
    @staticmethod
    def send_notification(employee_id, message):
        """Send a notification to the specified employee."""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9999))
        client.send(f"{employee_id}|{message}".encode('utf-8'))
        client.close()

class NotificationReceiver:
    @staticmethod
    def handle_client_connection(client_socket):
        """Handle incoming client connections."""
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received: {message}")
                employee_id, msg = message.split('|', 1)
                Notification(employee_id, msg).save()
        finally:
            client_socket.close()

    @staticmethod
    def start_server():
        """Start the notification server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 9999))
        server.listen(5)
        print("Server listening on port 9999")
        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=NotificationReceiver.handle_client_connection, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    NotificationReceiver.start_server()
