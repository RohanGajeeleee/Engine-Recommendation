import sys
import os
import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def start_server():
    from src.infrastructure.utils.database_initializer import clear_database, insert_initial_data
    from src.presentation.utils.client_handler import handle_client

    clear_database()
    insert_initial_data()

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
