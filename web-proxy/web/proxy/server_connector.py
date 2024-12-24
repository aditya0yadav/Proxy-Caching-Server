# web/proxy/server_connector.py
import socket
import ssl
from typing import Tuple, Optional
from web.config.settings import ServerConfig
from web.logging.logger import Logger

class ServerConnector:
    """Manage connections to target servers"""
    
    @staticmethod
    def connect_to_server(host: str, port: int = 80, use_ssl: bool = False) -> Optional[socket.socket]:
        """
        Establish connection to target server
        
        :param host: Target server hostname
        :param port: Target server port
        :param use_ssl: Whether to use SSL/HTTPS
        :return: Connected socket or None
        """
        try:
            # Create socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.settimeout(ServerConfig.CONNECTION_TIMEOUT)
            
            # Use SSL if required
            if use_ssl:
                context = ssl.create_default_context()
                server_socket = context.wrap_socket(
                    server_socket, 
                    server_hostname=host
                )
            
            # Connect to server
            server_socket.connect((host, port))
            
            return server_socket
        
        except Exception as e:
            Logger.log_error(f"Connection error to {host}:{port} - {e}")
            return None
    
    @staticmethod
    def send_request(sock: socket.socket, request: bytes) -> Optional[bytes]:
        """
        Send request to server and receive response
        
        :param sock: Connected socket
        :param request: Request bytes to send
        :return: Server response or None
        """
        try:
            # Send request
            sock.sendall(request)
            
            # Receive response
            response = b''
            while True:
                chunk = sock.recv(ServerConfig.BUFFER_SIZE)
                if not chunk:
                    break
                response += chunk
            
            return response
        
        except Exception as e:
            Logger.log_error(f"Request send error: {e}")
            return None
        finally:
            sock.close()