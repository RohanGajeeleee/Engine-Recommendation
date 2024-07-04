import logging
from src.application.services.request_handler import RequestHandler

def handle_client(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request: {request}")
        request_handler = RequestHandler()  # Create an instance
        response = request_handler.handle_request(request)  # Use the instance
        if response is None:
            response = "Invalid request"
        client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()
