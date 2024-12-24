import socket
import threading
from typing import Optional

from web.proxy.client_handler import ClientHandler
from web.config.settings import ServerConfig
from web.logging.logger import Logger

class ProxyServer:
    """Proxy server implementation"""
    
    def __init__(self, 
                 host: str = ServerConfig.HOST, 
                 port: int = ServerConfig.PORT):
        """
        Initialize proxy server
        
        :param host: Server host
        :param port: Server port
        """
        self._host = host
        self._port = port
        self._server_socket: Optional[socket.socket] = None
        self._client_handler = ClientHandler()
        self._is_running = False
    
    def start(self) -> None:
        """Start the proxy server"""
        try:
            # Create server socket
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server_socket.bind((self._host, self._port))
            self._server_socket.listen(ServerConfig.MAX_CONNECTIONS)
            
            self._is_running = True
            Logger.log_info(f"Proxy server started on {self._host}:{self._port}")
            
            # Accept client connections
            while self._is_running:
                try:
                    client_socket, address = self._server_socket.accept()
                    
                    # Handle client in a separate thread
                    client_thread = threading.Thread(
                        target=self._client_handler.handle_client, 
                        args=(client_socket,)
                    )
                    client_thread.start()
                
                except Exception as client_error:
                    Logger.log_error(f"Client connection error: {client_error}")
        
        except Exception as e:
            Logger.log_error(f"Proxy server error: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the proxy server"""
        self._is_running = False
        if self._server_socket:
            self._server_socket.close()
        Logger.log_info("Proxy server stopped")