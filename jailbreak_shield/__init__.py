"""
Jailbreak Shield v3.0 - Enterprise Prompt Injection Defense for Claude AI

Features:
    - 4-Layer Defense Grid (Reflex, Sentry, Oracle, Karma)
    - Local ML Support
    - Contextual Awareness
    - Metric & Caching
"""

from .shield import JailbreakShield
from .config import Config
from .layer1_static import StaticAnalyzer
from .layer2_sentry import SentryAnalyzer
from .layer3_oracle import SemanticAnalyzer
from .layer4_karma import KarmaTracker
from .cache import TTLCache
from .rate_limiter import RateLimiter
from .sanitizer import PromptSanitizer
from .metrics import MetricsCollector
from .logger import ShieldLogger

__version__ = "3.0.0"
__all__ = [
    "JailbreakShield",
    "Config",
    "StaticAnalyzer",
    "SentryAnalyzer",
    "SemanticAnalyzer",
    "KarmaTracker",
    "TTLCache",
    "RateLimiter",
    "PromptSanitizer",
    "MetricsCollector",
    "ShieldLogger"
]
