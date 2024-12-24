# web/proxy/request_parser.py
import urllib.parse
from typing import Dict, Any

class RequestParser:
    """Parse and process incoming HTTP requests"""
    
    @staticmethod
    def parse_request(request: bytes) -> Dict[str, Any]:
        """
        Parse raw HTTP request
        
        :param request: Raw request bytes
        :return: Parsed request dictionary
        """
        try:
            # Convert bytes to string
            request_str = request.decode('utf-8', errors='ignore')
            
            # Split request into lines
            lines = request_str.split('\n')
            if not lines:
                return {}
            
            # Parse request line
            method, full_url, _ = lines[0].split(' ')
            
            # Parse URL
            parsed_url = urllib.parse.urlparse(full_url)
            
            # Extract headers
            headers = {}
            for line in lines[1:]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
            
            return {
                'method': method,
                'url': full_url,
                'scheme': parsed_url.scheme,
                'host': parsed_url.hostname,
                'path': parsed_url.path,
                'headers': headers
            }
        except Exception as e:
            print(f"Error parsing request: {e}")
            return {}