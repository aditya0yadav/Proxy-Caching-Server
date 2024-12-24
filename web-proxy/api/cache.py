import functools
import json
import inspect
from typing import Callable, Any

class CacheManager:
    def __init__(self):
        self.cache = {}

    def _generate_cache_key(self, func: Callable, *args: Any, **kwargs: Any) -> str:
        if inspect.ismethod(func) or (inspect.isfunction(func) and len(inspect.signature(func).parameters) > 0):
            args = args[1:]  # Skip 'self'

        key_parts = [
            func.__name__,
            json.dumps(args, sort_keys=True),
            json.dumps(kwargs, sort_keys=True)
        ]
        return ':'.join(key_parts)

    def cached(self, ttl: int = 120):
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                key = self._generate_cache_key(func, *args, **kwargs)
                
                # Check if cached result exists and is not expired
                cached_result = self.cache.get(key)
                if cached_result:
                    return cached_result
                
                # Call the original function and cache the result
                result = await func(*args, **kwargs)
                self.cache[key] = result
                return result
            return wrapper
        return decorator

cache_manager = CacheManager()