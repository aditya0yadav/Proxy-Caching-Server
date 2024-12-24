PROJECT_NAME="web"

echo "Creating project structure for $PROJECT_NAME..."
mkdir -p $PROJECT_NAME

mkdir -p $PROJECT_NAME/config
mkdir -p $PROJECT_NAME/proxy
mkdir -p $PROJECT_NAME/cache
mkdir -p $PROJECT_NAME/security
mkdir -p $PROJECT_NAME/logging
mkdir -p $PROJECT_NAME/tests
mkdir -p $PROJECT_NAME/utils

touch $PROJECT_NAME/config/__init__.py
touch $PROJECT_NAME/config/settings.py
touch $PROJECT_NAME/config/cache_settings.py

touch $PROJECT_NAME/proxy/__init__.py
touch $PROJECT_NAME/proxy/server.py
touch $PROJECT_NAME/proxy/request_parser.py
touch $PROJECT_NAME/proxy/response_parser.py
touch $PROJECT_NAME/proxy/client_handler.py
touch $PROJECT_NAME/proxy/server_connector.py

touch $PROJECT_NAME/cache/__init__.py
touch $PROJECT_NAME/cache/cache_manager.py
touch $PROJECT_NAME/cache/cache_storage.py
touch $PROJECT_NAME/cache/cache_eviction.py
touch $PROJECT_NAME/security/__init__.py
touch $PROJECT_NAME/security/authentication.py
touch $PROJECT_NAME/security/url_blocking.py


touch $PROJECT_NAME/logging/__init__.py
touch $PROJECT_NAME/logging/logger.py
touch $PROJECT_NAME/logging/request_logger.py

touch $PROJECT_NAME/tests/__init__.py
touch $PROJECT_NAME/tests/test_server.py
touch $PROJECT_NAME/tests/test_cache.py
touch $PROJECT_NAME/tests/test_security.py
touch $PROJECT_NAME/tests/test_logging.py

touch $PROJECT_NAME/utils/__init__.py
touch $PROJECT_NAME/utils/timer.py
touch $PROJECT_NAME/utils/network_utils.py

touch $PROJECT_NAME/requirements.txt
touch $PROJECT_NAME/README.md
touch $PROJECT_NAME/main.py

echo "Project structure for $PROJECT_NAME created successfully!"
