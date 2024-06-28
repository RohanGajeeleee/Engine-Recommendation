import socket

def handle_client(client_socket):
    try:
        from src.application.services.request_handler import RequestHandler
        
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request: {request}")
        response = RequestHandler.handle_request(request)
        if response is None:
            response = "Invalid request"
        client_socket.send(response.encode('utf-8'))
    finally:
        client_socket.close()
