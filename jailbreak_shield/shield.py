"""
jailbreak_shield/shield.py

Main JailbreakShield class - the public API
"""

from typing import Dict, Optional
import os
from anthropic import Anthropic
from .layer1_static import StaticAnalyzer
from .layer2_semantic import SemanticAnalyzer
from .config import Config


class JailbreakShield:
    """
    Two-layer defense system against prompt injection attacks
    
    Usage:
        shield = JailbreakShield(api_key="your_anthropic_key")
        result = shield.defend("Your user prompt here")
        
        if result["safe"]:
            # Proceed with Claude API call
            response = claude.messages.create(...)
        else:
            # Block or sanitize
            print(f"Blocked: {result['explanation']}")
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        layer2_enabled: bool = True,
        layer2_threshold: float = 0.5
    ):
        """
        Initialize Jailbreak Shield
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            layer2_enabled: Enable Claude Haiku semantic analysis (default: True)
            layer2_threshold: Risk threshold to trigger Layer 2 (0-1, default: 0.5)
        """
        self.config = Config()
        self.layer1 = StaticAnalyzer()
        
        if layer2_enabled:
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY required for Layer 2")
            self.layer2 = SemanticAnalyzer(api_key)
        else:
            self.layer2 = None
        
        self.layer2_threshold = layer2_threshold
    
    def defend(self, prompt: str) -> Dict:
        """
        Analyze prompt for jailbreak attempts
        
        Args:
            prompt: User-provided prompt to analyze
        
        Returns:
            {
                "safe": bool,                    # True if safe to use
                "risk_score": float,             # 0-100 risk score
                "attack_detected": bool,         # True if attack found
                "attack_type": str or None,      # Type of attack detected
                "layer1_flagged": bool,          # Layer 1 result
                "layer2_flagged": bool or None,  # Layer 2 result (if used)
                "explanation": str,              # Human-readable explanation
                "recommendations": list,         # Mitigation recommendations
                "sanitized_prompt": str or None  # Cleaned version (if repairable)
            }
        """
        
        # Layer 1: Fast static analysis
        layer1_result = self.layer1.analyze(prompt)
        
        # If Layer 1 says safe OR Layer 2 disabled, return immediately
        if not layer1_result["suspicious"] or self.layer2 is None:
            return self._format_result(
                safe=not layer1_result["suspicious"],
                risk_score=layer1_result["risk_score"],
                attack_type=layer1_result.get("attack_type"),
                layer1_result=layer1_result,
                layer2_result=None
            )
        
        # Layer 2: Semantic analysis with Claude Haiku
        layer2_result = self.layer2.analyze(prompt, layer1_result)
        
        return self._format_result(
            safe=not layer2_result["malicious"],
            risk_score=layer2_result["risk_score"],
            attack_type=layer2_result.get("attack_type"),
            layer1_result=layer1_result,
            layer2_result=layer2_result
        )
    
    def _format_result(
        self,
        safe: bool,
        risk_score: float,
        attack_type: Optional[str],
        layer1_result: Dict,
        layer2_result: Optional[Dict]
    ) -> Dict:
        """Format final result dictionary"""
        
        return {
            "safe": safe,
            "risk_score": risk_score,
            "attack_detected": not safe,
            "attack_type": attack_type,
            "layer1_flagged": layer1_result["suspicious"],
            "layer2_flagged": layer2_result["malicious"] if layer2_result else None,
            "explanation": self._generate_explanation(
                safe, attack_type, layer1_result, layer2_result
            ),
            "recommendations": self._generate_recommendations(attack_type),
            "sanitized_prompt": self._sanitize(layer1_result) if not safe else None
        }
    
    def _generate_explanation(
        self,
        safe: bool,
        attack_type: Optional[str],
        layer1_result: Dict,
        layer2_result: Optional[Dict]
    ) -> str:
        """Generate human-readable explanation"""
        
        if safe:
            return "Prompt appears safe. No malicious patterns detected."
        
        explanation = f"⚠️ Potential jailbreak attempt detected: {attack_type}\n\n"
        
        if layer1_result.get("matched_patterns"):
            explanation += "Layer 1 detected:\n"
            for pattern in layer1_result["matched_patterns"]:
                explanation += f"  - {pattern['name']}: {pattern['description']}\n"
        
        if layer2_result and layer2_result.get("reasoning"):
            explanation += f"\nLayer 2 analysis:\n{layer2_result['reasoning']}"
        
        return explanation
    
    def _generate_recommendations(self, attack_type: Optional[str]) -> list:
        """Generate mitigation recommendations"""
        
        recommendations = [
            "Log this attempt for security audit",
            "Consider rate-limiting this user",
        ]
        
        if attack_type == "role_confusion":
            recommendations.append("Reinforce system prompt with role boundaries")
        elif attack_type == "context_injection":
            recommendations.append("Sanitize input for XML/markdown injection")
        elif attack_type == "payload_hiding":
            recommendations.append("Decode base64/unicode before analysis")
        
        return recommendations
    
    def _sanitize(self, layer1_result: Dict) -> Optional[str]:
        """Attempt to sanitize malicious prompt (basic implementation)"""
        # TODO: Implement smart sanitization
        return None
