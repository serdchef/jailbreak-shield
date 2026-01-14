"""
Jailbreak Shield - Prompt Injection Defense for Claude AI

Usage:
    from jailbreak_shield import JailbreakShield
    
    shield = JailbreakShield()
    result = shield.defend("Your prompt here")
    
    if result["safe"]:
        # Proceed with Claude API
    else:
        # Block or log
"""

from .shield import JailbreakShield
from .config import Config

__version__ = "0.1.0"
__all__ = ["JailbreakShield", "Config"]
