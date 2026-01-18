"""
tests/test_cache.py

Unit tests for TTL Cache
"""

import pytest
import time
from jailbreak_shield.cache import TTLCache, cached


class TestTTLCache:
    """Tests for TTLCache class"""
    
    def test_basic_get_set(self):
        """Test basic get/set operations"""
        cache = TTLCache(maxsize=100, ttl=60)
        
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
    
    def test_missing_key(self):
        """Test getting missing key returns None"""
        cache = TTLCache()
        assert cache.get("nonexistent") is None
    
    def test_ttl_expiration(self):
        """Test that items expire after TTL"""
        cache = TTLCache(maxsize=100, ttl=1)  # 1 second TTL
        
        cache.set("key", "value")
        assert cache.get("key") == "value"
        
        time.sleep(1.1)
        assert cache.get("key") is None
    
    def test_maxsize_eviction(self):
        """Test LRU eviction when cache is full"""
        cache = TTLCache(maxsize=3, ttl=60)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        
        # Adding 4th item should evict oldest
        cache.set("key4", "value4")
        
        assert cache.get("key1") is None  # Evicted
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"
    
    def test_delete(self):
        """Test delete operation"""
        cache = TTLCache()
        
        cache.set("key", "value")
        assert cache.delete("key") == True
        assert cache.get("key") is None
        assert cache.delete("key") == False
    
    def test_clear(self):
        """Test clear operation"""
        cache = TTLCache()
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        
        assert cache.get("key1") is None
        assert cache.get("key2") is None
    
    def test_stats(self):
        """Test statistics tracking"""
        cache = TTLCache(maxsize=100, ttl=60)
        
        cache.set("key", "value")
        cache.get("key")  # Hit
        cache.get("key")  # Hit
        cache.get("missing")  # Miss
        
        stats = cache.stats()
        assert stats["hits"] == 2
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 2/3
    
    def test_cleanup_expired(self):
        """Test cleanup of expired items"""
        cache = TTLCache(maxsize=100, ttl=1)
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        
        time.sleep(1.1)
        
        removed = cache.cleanup_expired()
        assert removed == 2


class TestCachedDecorator:
    """Tests for @cached decorator"""
    
    def test_caches_result(self):
        """Test that results are cached"""
        cache = TTLCache()
        call_count = 0
        
        @cached(cache)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = expensive_function(5)
        result2 = expensive_function(5)
        
        assert result1 == 10
        assert result2 == 10
        assert call_count == 1  # Only called once
    
    def test_different_args_not_cached(self):
        """Test that different args create separate cache entries"""
        cache = TTLCache()
        call_count = 0
        
        @cached(cache)
        def func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        func(1)
        func(2)
        func(1)  # Should be cached
        
        assert call_count == 2
