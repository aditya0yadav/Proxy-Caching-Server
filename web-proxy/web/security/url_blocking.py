# web/security/url_blocking.py
import re

class URLBlocker:
    """
    Manage URL blocking based on configuration
    """
    
    def __init__(self):
        """Initialize URL blocker with default blocked patterns"""
        self._blocked_patterns = [
            r'.*malicious\..*',
            r'.*porn\..*',
            r'.*gambling\..*'
        ]
    
    def is_blocked(self, url: str) -> bool:
        """
        Check if a URL is blocked
        
        :param url: URL to check
        :return: True if blocked, False otherwise
        """
        return any(
            re.match(pattern, url, re.IGNORECASE) 
            for pattern in self._blocked_patterns
        )
    
    def add_blocked_pattern(self, pattern: str) -> None:
        """
        Add a new URL blocking pattern
        
        :param pattern: Regex pattern to block
        """
        self._blocked_patterns.append(pattern)