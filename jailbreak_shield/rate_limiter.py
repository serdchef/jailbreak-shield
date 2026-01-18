"""
jailbreak_shield/rate_limiter.py

Token bucket rate limiter for per-user request throttling
"""

import time
import threading
from typing import Dict, Optional
from dataclasses import dataclass, field


@dataclass
class RateLimitResult:
    """Result of a rate limit check"""
    allowed: bool
    remaining: int
    reset_in: float
    limit: int
    
    def to_dict(self) -> Dict:
        return {
            "allowed": self.allowed,
            "remaining": self.remaining,
            "reset_in": round(self.reset_in, 2),
            "limit": self.limit
        }


@dataclass
class TokenBucket:
    """Token bucket for rate limiting"""
    tokens: float
    last_update: float
    rate: float  # tokens per second
    capacity: int
    
    def refill(self) -> None:
        """Refill tokens based on time elapsed"""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens, returns True if successful"""
        self.refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


class RateLimiter:
    """
    Per-user rate limiter using token bucket algorithm
    
    Usage:
        limiter = RateLimiter(requests_per_minute=60)
        
        result = limiter.check("user_123")
        if result.allowed:
            # Process request
        else:
            # Rate limited, wait result.reset_in seconds
    """
    
    def __init__(
        self,
        requests_per_minute: int = 60,
        burst_size: Optional[int] = None,
        cleanup_interval: int = 300
    ):
        """
        Initialize rate limiter
        
        Args:
            requests_per_minute: Sustained request rate
            burst_size: Maximum burst size (default: requests_per_minute)
            cleanup_interval: Seconds between cleanup of old buckets
        """
        self.rate = requests_per_minute / 60.0  # tokens per second
        self.capacity = burst_size or requests_per_minute
        self.cleanup_interval = cleanup_interval
        
        self._buckets: Dict[str, TokenBucket] = {}
        self._lock = threading.Lock()
        self._last_cleanup = time.time()
        
        # Statistics
        self._total_requests = 0
        self._rejected_requests = 0
    
    def check(self, user_id: str, tokens: int = 1) -> RateLimitResult:
        """
        Check if request is allowed for user
        
        Args:
            user_id: Unique identifier for the user
            tokens: Number of tokens to consume (default: 1)
        
        Returns:
            RateLimitResult with allowed status and metadata
        """
        with self._lock:
            self._maybe_cleanup()
            self._total_requests += 1
            
            # Get or create bucket
            if user_id not in self._buckets:
                self._buckets[user_id] = TokenBucket(
                    tokens=self.capacity,
                    last_update=time.time(),
                    rate=self.rate,
                    capacity=self.capacity
                )
            
            bucket = self._buckets[user_id]
            bucket.refill()
            
            if bucket.consume(tokens):
                return RateLimitResult(
                    allowed=True,
                    remaining=int(bucket.tokens),
                    reset_in=0,
                    limit=self.capacity
                )
            else:
                self._rejected_requests += 1
                # Calculate time until bucket has enough tokens
                tokens_needed = tokens - bucket.tokens
                reset_in = tokens_needed / self.rate
                
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_in=reset_in,
                    limit=self.capacity
                )
    
    def _maybe_cleanup(self) -> None:
        """Clean up old buckets periodically"""
        now = time.time()
        if now - self._last_cleanup < self.cleanup_interval:
            return
        
        self._last_cleanup = now
        
        # Remove buckets that haven't been used and are full
        stale_keys = []
        for user_id, bucket in self._buckets.items():
            bucket.refill()
            if bucket.tokens >= bucket.capacity:
                stale_keys.append(user_id)
        
        for key in stale_keys:
            del self._buckets[key]
    
    def reset(self, user_id: str) -> bool:
        """Reset rate limit for a specific user"""
        with self._lock:
            if user_id in self._buckets:
                del self._buckets[user_id]
                return True
            return False
    
    def stats(self) -> Dict:
        """Get rate limiter statistics"""
        with self._lock:
            rejection_rate = (
                self._rejected_requests / self._total_requests
                if self._total_requests > 0 else 0
            )
            
            return {
                "active_users": len(self._buckets),
                "total_requests": self._total_requests,
                "rejected_requests": self._rejected_requests,
                "rejection_rate": round(rejection_rate, 4),
                "rate_per_minute": self.rate * 60,
                "burst_capacity": self.capacity
            }


# Global default rate limiter
default_limiter = RateLimiter(requests_per_minute=60)
