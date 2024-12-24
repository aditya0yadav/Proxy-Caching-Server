# web/logging/request_logger.py
from typing import Dict, Any
from .logger import Logger

class RequestLogger:
    """
    Specialized logger for handling request-specific logging
    """
    
    @staticmethod
    def log_connection(client_address: str, method: str, url: str) -> None:
        """
        Log connection details
        
        :param client_address: IP address of client
        :param method: HTTP method
        :param url: Requested URL
        """
        log_message = f"Connection from {client_address}: {method} {url}"
        Logger.log_info(log_message)
    
    @staticmethod
    def log_error_response(client_address: str, error_code: int, error_message: str) -> None:
        """
        Log error responses
        
        :param client_address: IP address of client
        :param error_code: HTTP error code
        :param error_message: Error description
        """
        log_message = f"Error Response to {client_address}: {error_code} - {error_message}"
        Logger.log_error(log_message)
    
    @staticmethod
    def log_cache_event(event_type: str, url: str) -> None:
        """
        Log caching-related events
        
        :param event_type: Type of cache event (hit/miss/store)
        :param url: URL involved in cache event
        """
        log_message = f"Cache {event_type}: {url}"
        Logger.log_debug(log_message)