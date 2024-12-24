# web/logging/logger.py
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Dict, Any, Optional

class Logger:
    """
    Centralized logging system for the proxy server
    Supports file and console logging with multiple log levels
    """
    
    # Class variable to store logger instance
    _instance = None
    
    def __init__(self):
        """Initialize logging configuration"""
        # Create logs directory if not exists
        self._log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(self._log_dir, exist_ok=True)
        
        # Configure main logger
        self._logger = logging.getLogger('ProxyServerLogger')
        self._logger.setLevel(logging.INFO)
        
        # Clear any existing handlers
        self._logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler with rotation
        log_file_path = os.path.join(
            self._log_dir, 
            f'proxy_server_{datetime.now().strftime("%Y%m%d")}.log'
        )
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self._logger.addHandler(file_handler)
    
    @classmethod
    def get_instance(cls):
        """
        Singleton pattern implementation
        
        :return: Logger instance
        """
        if not cls._instance:
            cls._instance = Logger()
        return cls._instance
    
    @classmethod
    def log_info(cls, message: str) -> None:
        """
        Log an informational message
        
        :param message: Message to log
        """
        cls.get_instance()._logger.info(message)
    
    @classmethod
    def log_error(cls, message: str) -> None:
        """
        Log an error message
        
        :param message: Error message to log
        """
        cls.get_instance()._logger.error(message)
    
    @classmethod
    def log_debug(cls, message: str) -> None:
        """
        Log a debug message
        
        :param message: Debug message to log
        """
        cls.get_instance()._logger.debug(message)
    
    @classmethod
    def log_warning(cls, message: str) -> None:
        """
        Log a warning message
        
        :param message: Warning message to log
        """
        cls.get_instance()._logger.warning(message)
    
    @classmethod
    def log_request(cls, request: Dict[str, Any]) -> None:
        """
        Log details of an incoming request
        
        :param request: Request dictionary to log
        """
        request_log = f"Request: {request.get('method', 'UNKNOWN')} {request.get('url', 'N/A')}"
        cls.get_instance()._logger.info(request_log)
    
    @classmethod
    def configure(cls, log_level: Optional[str] = None) -> None:
        """
        Configure logger with specific log level
        
        :param log_level: Logging level (e.g., 'INFO', 'DEBUG', 'ERROR')
        """
        logger_instance = cls.get_instance()
        
        # Map log level strings to logging module levels
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        # Set log level
        if log_level and log_level.upper() in level_map:
            logger_instance._logger.setLevel(level_map[log_level.upper()])
        
        # Optional: Add more sophisticated logging configuration here