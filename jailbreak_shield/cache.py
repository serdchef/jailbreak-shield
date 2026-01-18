"""
jailbreak_shield/cache.py

LRU Cache with TTL support for prompt analysis results
"""

import time
import threading
from typing import Dict, Optional, Any
from collections import OrderedDict
from functools import wraps


class TTLCache:
    """
    Thread-safe LRU Cache with Time-To-Live support
    
    Usage:
        cache = TTLCache(maxsize=1000, ttl=300)  # 1000 items, 5 min TTL
        cache.set("key", value)
        result = cache.get("key")  # Returns None if expired or missing
    """
    
    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        """
        Initialize cache
        
        Args:
            maxsize: Maximum number of items to store
            ttl: Time-to-live in seconds (default: 5 minutes)
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self._cache: OrderedDict = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache, returns None if not found or expired"""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            value, timestamp = self._cache[key]
            
            # Check if expired
            if time.time() - timestamp > self.ttl:
                del self._cache[key]
                self._misses += 1
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self._hits += 1
            return value
    
    def set(self, key: str, value: Any) -> None:
        """Set item in cache with current timestamp"""
        with self._lock:
            # Remove existing if present
            if key in self._cache:
                del self._cache[key]
            
            # Evict oldest if at capacity
            while len(self._cache) >= self.maxsize:
                self._cache.popitem(last=False)
            
            # Add new item
            self._cache[key] = (value, time.time())
    
    def delete(self, key: str) -> bool:
        """Delete item from cache, returns True if existed"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def clear(self) -> None:
        """Clear all items from cache"""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def stats(self) -> Dict:
        """Get cache statistics"""
        with self._lock:
            total = self._hits + self._misses
            hit_rate = self._hits / total if total > 0 else 0
            
            return {
                "size": len(self._cache),
                "maxsize": self.maxsize,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "ttl": self.ttl
            }
    
    def cleanup_expired(self) -> int:
        """Remove all expired items, returns count removed"""
        with self._lock:
            now = time.time()
            expired_keys = [
                key for key, (_, timestamp) in self._cache.items()
                if now - timestamp > self.ttl
            ]
            for key in expired_keys:
                del self._cache[key]
            return len(expired_keys)


def cached(cache: TTLCache, key_func=None):
    """
    Decorator for caching function results
    
    Usage:
        cache = TTLCache()
        
        @cached(cache, key_func=lambda prompt: hash(prompt))
        def analyze(prompt):
            # expensive operation
            return result
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                key = str(key_func(*args, **kwargs))
            else:
                key = str(hash((args, tuple(sorted(kwargs.items())))))
            
            # Check cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result
        
        wrapper.cache = cache
        return wrapper
    
    return decorator


# Global default cache instance
default_cache = TTLCache(maxsize=1000, ttl=300)
