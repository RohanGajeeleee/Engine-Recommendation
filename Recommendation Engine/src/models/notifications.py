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
            if NotificationDatabaseHandler.employee_exists(employee[0]):
                Notification.send(employee[0], message)
            else:
                print(f"Error: Employee ID {employee[0]} does not exist.")

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
    
    @staticmethod
    def send_to_chef(message):
        chef_ids = NotificationDatabaseHandler.fetch_chefs()
        for chef_id in chef_ids:
            Notification.send(chef_id, message)

class NotificationDatabaseHandler:
    @staticmethod
    def fetch_notifications_by_item_name(item_name):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            # Update the search pattern to be more specific to feedback requests
            search_pattern = f"We are trying to improve your experience with {item_name}. Please provide your feedback and help us.%"
            
            query = "SELECT * FROM notifications WHERE message LIKE %s"
            cursor.execute(query, (search_pattern,))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
     
    @staticmethod
    def get_feedback_request_notifications():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT n.id, n.message
            FROM notifications n
            WHERE n.message LIKE 'We are trying to improve your experience%'
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def save_reply(notification_id, employee_id, reply):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM notification_replies WHERE notification_id = %s AND employee_id = %s"
            cursor.execute(query, (notification_id, employee_id))
            if cursor.fetchone()[0] > 0:
                print("You have already replied to this notification.")
                return

            query = "INSERT INTO notification_replies (notification_id, employee_id, reply, reply_date) VALUES (%s, %s, %s, NOW())"
            cursor.execute(query, (notification_id, employee_id, reply))
            db.commit()
            print("Reply saved successfully")
        except mysql.connector.Error as err:
            db.rollback()
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def user_has_replied(notification_id, employee_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM notification_replies WHERE notification_id = %s AND employee_id = %s"
            cursor.execute(query, (notification_id, employee_id))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()
    def get_latest_notification_id(item_name):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = """
            SELECT id FROM notifications 
            WHERE message LIKE %s 
            ORDER BY created_at DESC LIMIT 1
            """
            cursor.execute(query, (f'%{item_name}%',))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def get_feedback_replies():
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        try:
            query = """
            SELECT r.employee_id, r.reply, r.reply_date
            FROM notification_replies r
            JOIN notifications n ON r.notification_id = n.id
            WHERE n.message LIKE 'We are trying to improve your experience with%' 
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
        finally:
            cursor.close()
            db.close()
    @staticmethod
    def employee_exists(employee_id):
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT COUNT(*) FROM users WHERE employee_id = %s"
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            return result[0] > 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def save_notification(employee_id, message):
        if not NotificationDatabaseHandler.employee_exists(employee_id):
            print(f"Error: Employee ID {employee_id} does not exist.")
            return
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
    def fetch_chefs():
        db = get_db_connection()
        cursor = db.cursor()
        try:
            query = "SELECT employee_id FROM users WHERE role = 'chef'"
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
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
