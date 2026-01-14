"""
jailbreak_shield/layer1_static.py

Fast static pattern matching (10ms, no API cost)
"""

import re
from typing import Dict, List
from .patterns import ATTACK_PATTERNS


class StaticAnalyzer:
    """
    Static pattern-based analysis using regex and heuristics
    Detects known attack signatures without LLM calls
    """
    
    def __init__(self):
        self.patterns = ATTACK_PATTERNS
    
    def analyze(self, prompt: str) -> Dict:
        """
        Analyze prompt with static rules
        
        Returns:
            {
                "suspicious": bool,
                "risk_score": float (0-100),
                "matched_patterns": list,
                "attack_type": str or None
            }
        """
        
        matched = []
        max_risk = 0
        attack_type = None
        
        # Check each pattern
        for pattern in self.patterns:
            if self._check_pattern(prompt, pattern):
                matched.append(pattern)
                if pattern["risk"] > max_risk:
                    max_risk = pattern["risk"]
                    attack_type = pattern["category"]
        
        # Additional heuristics
        heuristic_risk = self._heuristic_analysis(prompt)
        final_risk = max(max_risk, heuristic_risk)
        
        return {
            "suspicious": final_risk >= 50,
            "risk_score": final_risk,
            "matched_patterns": matched,
            "attack_type": attack_type
        }
    
    def _check_pattern(self, prompt: str, pattern: Dict) -> bool:
        """Check if pattern matches"""
        
        if pattern["type"] == "regex":
            return bool(re.search(pattern["pattern"], prompt, re.IGNORECASE))
        
        elif pattern["type"] == "keyword":
            keywords = pattern["keywords"]
            prompt_lower = prompt.lower()
            return any(kw in prompt_lower for kw in keywords)
        
        elif pattern["type"] == "structure":
            # Check for structural anomalies
            return self._check_structure(prompt, pattern)
        
        return False
    
    def _check_structure(self, prompt: str, pattern: Dict) -> bool:
        """Check structural patterns (XML tags, excessive newlines, etc.)"""
        
        checks = {
            "excessive_newlines": prompt.count("\n") > 20,
            "xml_injection": bool(re.search(r"</?(system|user|assistant)>", prompt)),
            "unicode_abuse": len(re.findall(r"\\u[0-9a-fA-F]{4}", prompt)) > 5,
            "base64_suspicious": bool(re.search(r"[A-Za-z0-9+/]{50,}={0,2}", prompt))
        }
        
        return checks.get(pattern.get("check"), False)
    
    def _heuristic_analysis(self, prompt: str) -> float:
        """Additional heuristic checks beyond patterns"""
        
        risk = 0
        
        # Suspicious phrases
        suspicious_phrases = [
            "ignore previous",
            "forget everything",
            "you are now",
            "new instructions",
            "developer mode",
            "jailbreak",
            "unrestricted"
        ]
        
        for phrase in suspicious_phrases:
            if phrase in prompt.lower():
                risk += 20
        
        # Excessive length (possible injection)
        if len(prompt) > 5000:
            risk += 15
        
        # Repetitive patterns (confusion attack)
        words = prompt.split()
        if len(words) > 50:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:  # High repetition
                risk += 25
        
        return min(risk, 100)
