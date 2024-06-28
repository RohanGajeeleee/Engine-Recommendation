import socket
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_request(request):
   
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    client.send(request.encode('utf-8'))
    
    response = client.recv(1024).decode('utf-8')
    
    
    client.close()
    return response
