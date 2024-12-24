from web.proxy.server import ProxyServer
from web.config.settings import ServerConfig
from web.logging.logger import Logger

def main():
    """
    Main entry point for the proxy server application
    """
    try:
        # Configure logging
        Logger.configure(log_level=ServerConfig.LOG_LEVEL)
        
        # Create and start proxy server
        proxy_server = ProxyServer(
            host=ServerConfig.HOST, 
            port=ServerConfig.PORT
        )
        
        Logger.log_info("Starting proxy server...")
        proxy_server.start()
    
    except KeyboardInterrupt:
        Logger.log_info("Proxy server shutdown initiated by user")
    
    except Exception as e:
        Logger.log_error(f"Proxy server startup error: {e}")

if __name__ == "__main__":
    main()