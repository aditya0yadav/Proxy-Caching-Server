# web/cache/cache_storage.py
import time
from typing import Any, Dict, Optional
from collections import OrderedDict

class CacheStorage:
    """
    A flexible caching storage mechanism supporting 
    different storage types and eviction policies
    """
    
    def __init__(self, 
                 max_size: int = 1000, 
                 expiration_time: int = 3600, 
                 eviction_policy: str = 'least_recently_used'):
        """
        Initialize cache storage
        
        :param max_size: Maximum number of items in cache
        :param expiration_time: Time in seconds before cache item expires
        :param eviction_policy: Policy for removing items when cache is full
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = max_size
        self._expiration_time = expiration_time
        self._eviction_policy = eviction_policy
        
        # For LRU tracking
        self._access_order = OrderedDict()
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the cache
        
        :param key: Cache key
        :param value: Value to cache
        """
        # Remove expired entries
        self._clean_expired_entries()
        
        # Evict if cache is full
        if len(self._cache) >= self._max_size:
            self._evict_entry()
        
        # Store the entry with timestamp
        self._cache[key] = {
            'value': value,
            'timestamp': time.time()
        }
        
        # Update access order for LRU
        if key in self._access_order:
            del self._access_order[key]
        self._access_order[key] = None
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache
        
        :param key: Cache key
        :return: Cached value or None if not found/expired
        """
        entry = self._cache.get(key)
        
        if not entry:
            return None
        print(self._cache)
        
        # Check for expiration
        if time.time() - entry['timestamp'] > self._expiration_time:
            del self._cache[key]
            return None
        
        # Update access order for LRU
        if self._eviction_policy == 'least_recently_used':
            del self._access_order[key]
            self._access_order[key] = None
        
        return entry['value']
    
    def _clean_expired_entries(self) -> None:
        """Remove all expired entries from cache"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if current_time - entry['timestamp'] > self._expiration_time
        ]
        
        for key in expired_keys:
            del self._cache[key]
            if key in self._access_order:
                del self._access_order[key]
    
    def _evict_entry(self) -> None:
        """Evict an entry based on the selected policy"""
        if not self._cache:
            return
        
        if self._eviction_policy == 'least_recently_used':
            # Remove the least recently used item
            lru_key = next(iter(self._access_order))
            del self._cache[lru_key]
            del self._access_order[lru_key]
        
        elif self._eviction_policy == 'first_in_first_out':
            # Find and remove the oldest entry
            oldest_key = min(
                self._cache, 
                key=lambda k: self._cache[k]['timestamp']
            )
            del self._cache[oldest_key]
    
    def clear(self) -> None:
        """Clear entire cache"""
        self._cache.clear()
        self._access_order.clear()
    
    def __len__(self) -> int:
        """Return number of items in cache"""
        return len(self._cache)