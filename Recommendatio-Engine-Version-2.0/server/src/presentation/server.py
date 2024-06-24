import sys
import os
import socket
import threading

# Adjust the path to include the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.application.services.user_service import UserService

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        response = UserService.handle_request(request)
        client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()

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
