import sys
import os
import socket
import threading
import mysql.connector
# Adjust the path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.application.services.user_service import UserService
from src.infrastructure.repositories.menu_item_repository import MenuItemRepository
from src.domain.models.menu_item import MenuItem


def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request: {request}")
        response = handle_request(request)
        if response is None:
            response = "Invalid request"
        client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()

def handle_request(request):
    parts = request.split()
    command = parts[0]

    if command == "REGISTER":
        if len(parts) != 5:
            return "Invalid REGISTER command format"
        _, employee_id, name, password, role = parts
        UserService.register_user(employee_id, name, password, role)
        return "User registered successfully"

    elif command == "AUTH":
        if len(parts) != 3:
            return "Invalid AUTH command format"
        _, employee_id, password = parts
        role = UserService.authenticate_user(employee_id, password)
        if role:
            return f"Authenticated as {role}"
        return "Authentication failed"

    elif command == "ADD_ITEM":
        if len(parts) != 4:
            return "Invalid ADD_ITEM command format"
        _, name, price, availability = parts
        MenuItemRepository.add(MenuItem(name=name, price=float(price), availability=availability))
        return "Menu item added successfully"

    elif command == "UPDATE_ITEM":
        if len(parts) != 5:
            return "Invalid UPDATE_ITEM command format"
        _, item_id, name, price, availability = parts
        item_id = int(item_id)
        name = None if name == "null" else name
        price = None if price == "null" else float(price)
        availability = None if availability == "null" else availability
        MenuItemRepository.update(MenuItem(item_id=item_id, name=name, price=price, availability=availability))
        return "Menu item updated successfully"

    elif command == "DELETE_ITEM":
        if len(parts) != 2:
            return "Invalid DELETE_ITEM command format"
        _, item_id = parts
        item_id = int(item_id)
        try:
            MenuItemRepository.delete(item_id)
            return "Menu item deleted successfully"
        except mysql.connector.Error as err:
            if err.errno == 1451:
                return f"Error: Cannot delete item ID {item_id} due to foreign key constraints"
            else:
                return f"Error: {err}"

    elif command == "VIEW_MENU":
        items = MenuItemRepository.get_all()
        if items:
            response = "\nMenu Items:\n"
            for item in items:
                response += f"ID: {item['id']}, Name: {item['name']}, Price: {item['price']}, Availability: {item['availability']}\n"
            return response
        return "No menu items available"

    else:
        return "INVALID REQUEST"


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server listening on port 9999")
    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
