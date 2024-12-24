# web/config/settings.py
class ServerConfig:
    """Server configuration settings"""
    
    # Proxy server settings
    HOST = '127.0.0.1'
    PORT = 8080
    
    # Connection settings
    BUFFER_SIZE = 4096
    MAX_CONNECTIONS = 100
    
    # Timeout settings
    CONNECTION_TIMEOUT = 10  # seconds
    READ_TIMEOUT = 30  # seconds
    
    # Logging settings
    LOG_LEVEL = 'INFO'
    
    # Caching settings
    ENABLE_CACHING = True
    CACHE_TIMEOUT = 3600  # 1 hour