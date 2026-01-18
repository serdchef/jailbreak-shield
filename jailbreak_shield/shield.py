"""
jailbreak_shield/shield.py

Main JailbreakShield class - Enterprise-grade defense API
Features: 4-Layer Defense Grid (Reflex, Sentry, Oracle, Karma)
"""

import os
import time
import hashlib
import asyncio
from typing import Dict, Optional, Union
from concurrent.futures import ThreadPoolExecutor

from .layer1_static import StaticAnalyzer
from .layer2_sentry import SentryAnalyzer
from .layer3_oracle import SemanticAnalyzer
from .layer4_karma import KarmaTracker
from .config import Config
from .cache import TTLCache
from .rate_limiter import RateLimiter, RateLimitResult
from .sanitizer import PromptSanitizer
from .metrics import MetricsCollector
from .logger import ShieldLogger, SecurityEvent


class JailbreakShield:
    """
    Enterprise-grade 4-layer defense system against prompt injection attacks
    
    Layers:
        1. Reflex (Static): Regex & Heuristics (<1ms)
        2. Sentry (Local ML): BERT/Transformers (<50ms)
        3. Oracle (Semantic): Claude Haiku (Deep Analysis)
        4. Karma  (Context): Behavioral History
    """
    
    VERSION = "3.0.0"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        layer2_enabled: bool = True,  # Sentry (Local ML)
        layer3_enabled: bool = True,  # Oracle (Claude)
        layer4_enabled: bool = True,  # Karma (Context)
        # Cache options
        cache_enabled: bool = True,
        cache_size: int = 1000,
        cache_ttl: int = 300,
        # Rate limiting options
        rate_limit_enabled: bool = False,
        rate_limit_rpm: int = 60,
        # Logging options
        log_enabled: bool = True,
        log_json: bool = True,
        log_file: Optional[str] = None,
        # Metrics options
        metrics_enabled: bool = True,
    ):
        self.config = Config()
        
        # --- LAYER 1: REFLEX (Static) ---
        self.layer1 = StaticAnalyzer()
        
        # --- LAYER 2: SENTRY (Local ML) ---
        self.layer2_enabled = layer2_enabled
        self.layer2 = SentryAnalyzer() if layer2_enabled else None
        
        # --- LAYER 3: ORACLE (Semantic) ---
        self.layer3_enabled = layer3_enabled
        if layer3_enabled:
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            # Don't crash if API key missing, just disable L3
            if api_key:
                self.layer3 = SemanticAnalyzer(api_key)
            else:
                print("⚠️ Warning: No API key for Layer 3 (Oracle). Layer disabled.")
                self.layer3 = None
                self.layer3_enabled = False
        else:
            self.layer3 = None
            
        # --- LAYER 4: KARMA (Context) ---
        self.layer4_enabled = layer4_enabled
        self.layer4 = KarmaTracker() if layer4_enabled else None
        self.layer4_threshold = 60.0 # Below this is suspicious
        
        # Utilities
        self.cache_enabled = cache_enabled
        self.cache = TTLCache(maxsize=cache_size, ttl=cache_ttl) if cache_enabled else None
        
        self.rate_limit_enabled = rate_limit_enabled
        self.rate_limiter = RateLimiter(requests_per_minute=rate_limit_rpm) if rate_limit_enabled else None
        
        self.sanitizer = PromptSanitizer()
        
        self.metrics_enabled = metrics_enabled
        self.metrics = MetricsCollector() if metrics_enabled else None
        
        self.logger = ShieldLogger(json_output=log_json, log_file=log_file) if log_enabled else None
        
        self._executor = ThreadPoolExecutor(max_workers=4)
    
    def defend(
        self,
        prompt: str,
        user_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze prompt using 4-layer defense grid
        """
        start_time = time.time()
        
        # 0. Rate limiting
        if self.rate_limit_enabled and user_id:
            rate_result = self.rate_limiter.check(user_id)
            if not rate_result.allowed:
                return self._rate_limited_response(rate_result)
        
        # 1. Cache Check
        prompt_hash = self._hash_prompt(prompt)
        if self.cache_enabled:
            cached = self.cache.get(prompt_hash)
            if cached:
                cached["cached"] = True
                cached["latency_ms"] = (time.time() - start_time) * 1000
                return cached
                
        # --- LAYER 4: KARMA (Pre-check) ---
        # We check Karma FIRST to catch blocked users immediately
        karma_result = None
        if self.layer4_enabled and user_id:
             karma_result = self.layer4.analyze(user_id, prompt)
             if karma_result["suspicious"]:
                 pass # We mark it but continue analysis to categorize detection
                 
        # --- LAYER 1: REFLEX ---
        l1_start = time.time()
        l1_result = self.layer1.analyze(prompt)
        l1_lat = (time.time() - l1_start) * 1000
        
        # --- LAYER 2: SENTRY ---
        l2_result = None
        l2_lat = 0
        if self.layer2_enabled:
            l2_start = time.time()
            l2_result = self.layer2.analyze(prompt)
            l2_lat = (time.time() - l2_start) * 1000
            
        # Decision Logic: Should we call Layer 3 (Oracle)?
        # Call L3 if:
        # 1. L1 is suspicious OR
        # 2. L2 is suspicious OR
        # 3. Karma is low
        
        l3_result = None
        l3_lat = 0
        should_call_oracle = (
            l1_result["suspicious"] or 
            (l2_result and l2_result["suspicious"]) or 
            (karma_result and karma_result["suspicious"])
        )
        
        if self.layer3_enabled and should_call_oracle:
            l3_start = time.time()
            # Pass results of previous layers to give context
            l3_result = self.layer3.analyze(prompt, {
                "layer1": l1_result,
                "layer2": l2_result,
                "karma": karma_result
            })
            l3_lat = (time.time() - l3_start) * 1000
            
        # --- FINAL VERDICT ---
        # Safe if:
        # - L3 said safe (highest authority)
        # - OR L3 wasn't called AND L1/L2/Karma were safe
        
        is_safe = True
        risk_score = 0.0
        primary_layer = "none"
        attack_type = None
        
        if l3_result:
            is_safe = not l3_result["malicious"]
            risk_score = l3_result["risk_score"]
            attack_type = l3_result.get("attack_type")
            primary_layer = "oracle"
        else:
            # Aggregate risk from L1/L2/Karma
            risks = []
            if l1_result: risks.append(l1_result["risk_score"])
            if l2_result: risks.append(l2_result["risk_score"])
            if karma_result: risks.append(karma_result["risk_score"])
            
            risk_score = max(risks) if risks else 0
            is_safe = risk_score < 50
            
            if not is_safe:
                # determine who caught it
                if l1_result["suspicious"]: 
                    primary_layer = "reflex"
                    attack_type = l1_result.get("attack_type")
                elif l2_result and l2_result["suspicious"]: 
                    primary_layer = "sentry"
                    attack_type = l2_result.get("attack_type")
                elif karma_result and karma_result["suspicious"]: 
                    primary_layer = "karma"
                    attack_type = "social_engineering"
        
        # Update Karma (Post-analysis)
        if self.layer4_enabled and user_id:
            self.layer4.add_event(user_id, prompt, risk_score, attack_type)
            
        # Format Result
        total_lat = (time.time() - start_time) * 1000
        
        result = {
            "safe": is_safe,
            "risk_score": risk_score,
            "attack_type": attack_type,
            "primary_layer": primary_layer,
            "latency_ms": total_lat,
            "cached": False,
            "layers": {
                "reflex": l1_result,
                "sentry": l2_result,
                "oracle": l3_result,
                "karma": karma_result
            },
            "latencies": {
                "reflex": l1_lat,
                "sentry": l2_lat,
                "oracle": l3_lat
            },
            "explanation": self._generate_explanation(is_safe, attack_type, primary_layer),
            "recommendations": [] # Simplified for now
        }
        
        # Cache & Metrics
        if self.cache_enabled: self.cache.set(prompt_hash, result)
        if self.metrics_enabled: self.metrics.record_latency("total", total_lat / 1000)
        
        return result

    def _hash_prompt(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()[:16]

    def _rate_limited_response(self, rate_result) -> Dict:
        return {"safe": False, "risk_score": 0, "error": "rate_limit_exceeded"}
        
    def _generate_explanation(self, safe: bool, attack_type: str, layer: str) -> str:
        if safe: return "Prompt analysis passed. No threats detected."
        return f"Blocked by {layer.upper()} Layer. Detected: {attack_type}."

    def get_stats(self) -> Dict:
        """
        Returns current shield statistics and metrics.
        
        Returns:
            Dict containing layer status, cache stats, and performance metrics.
        """
        stats = {
            "version": "3.0.0",
            "layers": {
                "L1_REFLEX": {"enabled": True, "status": "active"},
                "L2_SENTRY": {"enabled": self.layer2_enabled, "status": "active" if self.layer2_enabled else "disabled"},
                "L3_ORACLE": {"enabled": self.layer3_enabled, "status": "active" if self.layer3_enabled else "disabled"},
                "L4_KARMA": {"enabled": self.layer4_enabled, "status": "active" if self.layer4_enabled else "disabled"},
            },
            "cache": {
                "enabled": self.cache_enabled,
                "size": self.cache.stats()["size"] if self.cache else 0,
                "max_size": self.cache.maxsize if self.cache else 0,
            },
            "rate_limiter": {
                "enabled": self.rate_limit_enabled,
            },
        }
        
        if self.metrics_enabled and self.metrics:
            stats["metrics"] = self.metrics.get_summary()
        
        return stats
