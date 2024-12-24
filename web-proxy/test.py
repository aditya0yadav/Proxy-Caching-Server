# test_client.py
import socket

def test_proxy_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))
    
    # Send a test request
    request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    client_socket.send(request.encode())
    
    # Receive response
    response = client_socket.recv(4096)
    print(response.decode())
    
    client_socket.close()

if __name__ == "__main__":
    test_proxy_server()