from typing import Dict, Any, Callable

class CacheEvictionStrategy:
    """
    Advanced cache eviction strategies
    """
    
    @staticmethod
    def least_recently_used(cache: Dict[str, Dict[str, Any]], 
                             max_size: int) -> str:
        """
        Identify least recently used item for eviction
        
        :param cache: Current cache dictionary
        :param max_size: Maximum cache size
        :return: Key of item to evict
        """
        return min(
            cache, 
            key=lambda k: cache[k].get('last_accessed', 0)
        )
    
    @staticmethod
    def first_in_first_out(cache: Dict[str, Dict[str, Any]], 
                            max_size: int) -> str:
        """
        Identify first added item for eviction
        
        :param cache: Current cache dictionary
        :param max_size: Maximum cache size
        :return: Key of item to evict
        """
        return min(
            cache, 
            key=lambda k: cache[k].get('created_at', 0)
        )
    
    @staticmethod
    def least_frequently_used(cache: Dict[str, Dict[str, Any]], 
                               max_size: int) -> str:
        """
        Identify least frequently accessed item for eviction
        
        :param cache: Current cache dictionary
        :param max_size: Maximum cache size
        :return: Key of item to evict
        """
        return min(
            cache, 
            key=lambda k: cache[k].get('access_count', 0)
        )
    
    @classmethod
    def get_strategy(cls, strategy_name: str) -> Callable:
        """
        Get eviction strategy by name
        
        :param strategy_name: Name of eviction strategy
        :return: Eviction strategy function
        """
        strategies = {
            'least_recently_used': cls.least_recently_used,
            'first_in_first_out': cls.first_in_first_out,
            'least_frequently_used': cls.least_frequently_used
        }
        
        return strategies.get(
            strategy_name, 
            cls.least_recently_used  # Default strategy
        )