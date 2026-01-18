"""
tests/test_rate_limiter.py

Unit tests for Rate Limiter
"""

import pytest
import time
from jailbreak_shield.rate_limiter import RateLimiter, RateLimitResult


class TestRateLimiter:
    """Tests for RateLimiter class"""
    
    def test_allows_within_limit(self):
        """Test that requests within limit are allowed"""
        limiter = RateLimiter(requests_per_minute=60)
        
        result = limiter.check("user1")
        assert result.allowed == True
        assert result.remaining > 0
    
    def test_blocks_over_limit(self):
        """Test that requests over limit are blocked"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=5)
        
        # Use up all tokens
        for _ in range(5):
            limiter.check("user1")
        
        result = limiter.check("user1")
        assert result.allowed == False
        assert result.remaining == 0
        assert result.reset_in > 0
    
    def test_separate_users(self):
        """Test that different users have separate limits"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=3)
        
        # User 1 uses all tokens
        for _ in range(3):
            limiter.check("user1")
        
        # User 2 should still be allowed
        result = limiter.check("user2")
        assert result.allowed == True
    
    def test_token_refill(self):
        """Test that tokens refill over time"""
        limiter = RateLimiter(requests_per_minute=120, burst_size=2)  # 2 tokens/sec
        
        # Use both tokens
        limiter.check("user1")
        limiter.check("user1")
        
        # Should be blocked
        result = limiter.check("user1")
        assert result.allowed == False
        
        # Wait for refill
        time.sleep(1)
        
        # Should be allowed again
        result = limiter.check("user1")
        assert result.allowed == True
    
    def test_reset_user(self):
        """Test resetting a specific user's limit"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=1)
        
        limiter.check("user1")
        result = limiter.check("user1")
        assert result.allowed == False
        
        limiter.reset("user1")
        
        result = limiter.check("user1")
        assert result.allowed == True
    
    def test_stats(self):
        """Test statistics tracking"""
        limiter = RateLimiter(requests_per_minute=60, burst_size=2)
        
        limiter.check("user1")
        limiter.check("user1")
        limiter.check("user1")  # Should be rejected
        
        stats = limiter.stats()
        assert stats["total_requests"] == 3
        assert stats["rejected_requests"] == 1
        assert stats["active_users"] == 1
    
    def test_result_to_dict(self):
        """Test RateLimitResult.to_dict()"""
        result = RateLimitResult(
            allowed=True,
            remaining=5,
            reset_in=0,
            limit=10
        )
        
        d = result.to_dict()
        assert d["allowed"] == True
        assert d["remaining"] == 5
