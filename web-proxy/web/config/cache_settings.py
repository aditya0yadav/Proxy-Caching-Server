
class CacheConfig:
    """Configuration for caching mechanism"""
    
    DEFAULT_CACHE_SIZE = 1000
    
    DEFAULT_EXPIRATION_TIME = 360  # 1 hour
    
    STORAGE_MEMORY = 'memory'
    STORAGE_DISK = 'disk'
    
    DEFAULT_STORAGE_TYPE = STORAGE_MEMORY
    
    EVICTION_LRU = 'least_recently_used'
    EVICTION_FIFO = 'first_in_first_out'
    
    DEFAULT_EVICTION_POLICY = EVICTION_LRU