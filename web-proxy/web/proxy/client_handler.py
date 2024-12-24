import socket
from typing import Tuple
from web.proxy.request_parser import RequestParser
from web.proxy.server_connector import ServerConnector
from web.config.settings import ServerConfig
from web.cache.cache_manager import CacheManager
from web.logging.logger import Logger
from web.security.url_blocking import URLBlocker

class ClientHandler:
    """Handle client connections and requests"""
    
    def __init__(self):
        """Initialize client handler"""
        self._cache_manager = CacheManager()
        self._url_blocker = URLBlocker()
    
    def handle_client(self, client_socket: socket.socket) -> None:
        """
        Handle individual client connection
        
        :param client_socket: Connected client socket
        """
        try:
            # Receive client request
            request = client_socket.recv(ServerConfig.BUFFER_SIZE)
            print(request)

            # Parse request
            parsed_request = RequestParser.parse_request(request)
            print(parsed_request)
            
            # Check URL blocking
            if self._url_blocker.is_blocked(parsed_request.get('url', '')):
                self._send_blocked_response(client_socket)
                return
            
            # Check cache
            response = None
            if ServerConfig.ENABLE_CACHING:
                response = self._cache_manager.retrieve(parsed_request.get('url', ''))
            
            # If cache is not available, try localhost
            if not response:
                try:
                    # Attempt to fetch from localhost
                    localhost_socket = ServerConnector.connect_to_server('localhost', port=7070)
                    if localhost_socket:
                        response = ServerConnector.send_request(localhost_socket, request)
                        localhost_socket.close()
                except Exception as localhost_error:
                    Logger.log_error(f"Localhost fetch error: {localhost_error}")
            
            # If localhost fails, connect to target server
            if not response:
                server_socket = ServerConnector.connect_to_server(
                    parsed_request.get('host', ''),
                    port=443 if parsed_request.get('scheme') == 'https' else 80
                )
                
                if not server_socket:
                    self._send_error_response(client_socket)
                    return
                
                # Forward request and get response
                response = ServerConnector.send_request(server_socket, request)
            
            if response:
                # Cache response if enabled and not already in cache
                if ServerConfig.ENABLE_CACHING:
                    self._cache_manager.cache(
                        parsed_request.get('url', ''), 
                        response
                    )
                
                # Send response to client
                client_socket.sendall(response)
            else:
                self._send_error_response(client_socket)
            
            # Log request
            Logger.log_request(parsed_request)
        
        except Exception as e:
            Logger.log_error(f"Client handler error: {e}")
            self._send_error_response(client_socket)
        finally:
            client_socket.close()
    
    def _send_blocked_response(self, socket: socket.socket) -> None:
        """Send response for blocked URL"""
        response = b"HTTP/1.1 403 Forbidden\r\nContent-Type: text/plain\r\n\r\nURL is blocked"
        socket.sendall(response)
    
    def _send_error_response(self, socket: socket.socket) -> None:
        """Send error response"""
        response = b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\r\nProxy error occurred"
        socket.sendall(response)