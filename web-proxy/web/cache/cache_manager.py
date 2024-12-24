# web/cache/cache_manager.py
from typing import Any, Optional
from .cache_storage import CacheStorage
from ..config.cache_settings import CacheConfig

class CacheManager:
    """
    Centralized cache management with configurable storage
    """
    
    def __init__(self, 
                 max_size: int = CacheConfig.DEFAULT_CACHE_SIZE,
                 expiration_time: int = CacheConfig.DEFAULT_EXPIRATION_TIME,
                 eviction_policy: str = CacheConfig.DEFAULT_EVICTION_POLICY):
        """
        Initialize cache manager
        
        :param max_size: Maximum cache size
        :param expiration_time: Cache entry expiration time
        :param eviction_policy: Cache eviction strategy
        """
        self._storage = CacheStorage(
            max_size=max_size,
            expiration_time=expiration_time,
            eviction_policy=eviction_policy
        )
    
    def cache(self, key: str, value: Any) -> None:
        """
        Cache a value with given key
        
        :param key: Unique cache key
        :param value: Value to cache
        """
        self._storage.set(key, value)
    
    def retrieve(self, key: str) -> Optional[Any]:
        """
        Retrieve a cached value
        
        :param key: Cache key to retrieve
        :return: Cached value or None if not found
        """
        return self._storage.get(key)
    
    def invalidate(self, key: str) -> None:
        """
        Remove a specific entry from cache
        
        :param key: Key to remove
        """
        if key in self._storage._cache:
            del self._storage._cache[key]
    
    def clear_cache(self) -> None:
        """Clear entire cache"""
        self._storage.clear()
    
    @property
    def cache_size(self) -> int:
        """
        Get current cache size
        
        :return: Number of items in cache
        """
        return len(self._storage)