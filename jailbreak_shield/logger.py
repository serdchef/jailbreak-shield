"""
jailbreak_shield/logger.py

Structured JSON logging for security events and audit trails
"""

import json
import logging
import sys
from datetime import datetime
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class SecurityEvent:
    """Structured security event for logging"""
    timestamp: str
    event_type: str
    user_id: Optional[str]
    prompt_hash: str
    risk_score: float
    attack_type: Optional[str]
    blocked: bool
    layer1_result: bool
    layer2_result: Optional[bool]
    latency_ms: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add extra fields if present
        if hasattr(record, "event"):
            log_data["event"] = record.event
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "risk_score"):
            log_data["risk_score"] = record.risk_score
        if hasattr(record, "attack_type"):
            log_data["attack_type"] = record.attack_type
        if hasattr(record, "metadata"):
            log_data["metadata"] = record.metadata
            
        return json.dumps(log_data)


class ShieldLogger:
    """
    Centralized logger for Jailbreak Shield with structured output
    
    Usage:
        logger = ShieldLogger("shield.security")
        logger.log_detection(event)
        logger.log_blocked(user_id, prompt_hash, reason)
    """
    
    def __init__(
        self,
        name: str = "jailbreak_shield",
        level: int = logging.INFO,
        json_output: bool = True,
        log_file: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.json_output = json_output
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        if json_output:
            console_handler.setFormatter(JSONFormatter())
        else:
            console_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(JSONFormatter())
            self.logger.addHandler(file_handler)
    
    def log_detection(self, event: SecurityEvent) -> None:
        """Log a security detection event"""
        extra = {
            "event": event.to_dict(),
            "user_id": event.user_id,
            "risk_score": event.risk_score,
            "attack_type": event.attack_type
        }
        
        if event.blocked:
            self.logger.warning(
                f"BLOCKED: {event.attack_type or 'unknown'} (risk: {event.risk_score})",
                extra=extra
            )
        else:
            self.logger.info(
                f"ALLOWED: risk_score={event.risk_score}",
                extra=extra
            )
    
    def log_blocked(
        self,
        user_id: Optional[str],
        prompt_hash: str,
        reason: str,
        risk_score: float
    ) -> None:
        """Log a blocked request"""
        self.logger.warning(
            f"Request blocked: {reason}",
            extra={
                "event": "blocked",
                "user_id": user_id,
                "prompt_hash": prompt_hash,
                "risk_score": risk_score
            }
        )
    
    def log_allowed(
        self,
        user_id: Optional[str],
        prompt_hash: str,
        risk_score: float
    ) -> None:
        """Log an allowed request"""
        self.logger.info(
            f"Request allowed: risk_score={risk_score}",
            extra={
                "event": "allowed",
                "user_id": user_id,
                "prompt_hash": prompt_hash,
                "risk_score": risk_score
            }
        )
    
    def log_error(self, error: Exception, context: Optional[Dict] = None) -> None:
        """Log an error"""
        self.logger.error(
            f"Error: {str(error)}",
            extra={"event": "error", "metadata": context or {}}
        )
    
    def log_rate_limited(self, user_id: str, reset_in: float) -> None:
        """Log a rate-limited request"""
        self.logger.warning(
            f"Rate limited: user={user_id}, reset_in={reset_in}s",
            extra={"event": "rate_limited", "user_id": user_id}
        )


# Global default logger
default_logger = ShieldLogger()
