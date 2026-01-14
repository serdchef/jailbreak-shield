"""
jailbreak_shield/config.py

Configuration management
"""

import os
from typing import Optional


class Config:
    """Configuration for Jailbreak Shield"""
    
    def __init__(self):
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.layer2_enabled = os.getenv("LAYER2_ENABLED", "true").lower() == "true"
        self.layer2_threshold = float(os.getenv("LAYER2_THRESHOLD", "0.5"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self):
        """Validate configuration"""
        if self.layer2_enabled and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY required when Layer 2 is enabled")
