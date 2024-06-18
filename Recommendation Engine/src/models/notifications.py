import sys
import os
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
        NotificationDatabaseHandler.save_notification(self.employee_id, self.message)

    @staticmethod
    def send(employee_id, message):
        NotificationSender.send_notification(employee_id, message)

    @staticmethod
    def send_to_all_employees(message):
        employees = NotificationDatabaseHandler.fetch_all_employees()
        for employee in employees:
            Notification.send(employee[0], message)

    @staticmethod
    def handle_client(client_socket):
        NotificationReceiver.handle_client_connection(client_socket)

    @staticmethod
    def start_server():
        NotificationReceiver.start_server()

    @staticmethod
    def fetch_and_clear_notifications(employee_id):
        notifications = NotificationDatabaseHandler.fetch_notifications(employee_id)
        NotificationDatabaseHandler.clear_notifications(employee_id, notifications)
        return notifications

class NotificationDatabaseHandler:
    @staticmethod
    def save_notification(employee_id, message):
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
    def update_notification(employee_id, message):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "UPDATE notifications SET message = %s WHERE employee_id = %s"
            cursor.execute(query, (message, employee_id))
            db.commit()
            print("Notification updated successfully")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def fetch_notifications(employee_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT id, message FROM notifications WHERE employee_id = %s AND is_read = 0"
            cursor.execute(query, (employee_id,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def clear_notifications(employee_id, notifications):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            notification_ids = [n['id'] for n in notifications]
            if notification_ids:
                format_strings = ','.join(['%s'] * len(notification_ids))
                query = f"UPDATE notifications SET is_read = 1 WHERE employee_id = %s AND id IN ({format_strings})"
                cursor.execute(query, [employee_id] + notification_ids)
                db.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def fetch_all_employees():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT employee_id FROM users WHERE role = 'employee'"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()

class NotificationSender:
    @staticmethod
    def send_notification(employee_id, message):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 9999))
        client.send(f"{employee_id}|{message}".encode('utf-8'))
        client.close()

class NotificationReceiver:
    @staticmethod
    def handle_client_connection(client_socket):
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
