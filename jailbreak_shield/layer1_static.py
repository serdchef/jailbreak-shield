"""
jailbreak_shield/layer1_static.py

Fast static pattern matching with advanced detection capabilities
Supports: multilingual, homoglyphs, leetspeak, invisible chars
"""

import re
import unicodedata
from typing import Dict, List, Set
from functools import lru_cache
from .patterns import ATTACK_PATTERNS, SEVERITY_LEVELS


class StaticAnalyzer:
    """
    Static pattern-based analysis using regex and heuristics
    Detects known attack signatures without LLM calls
    
    Features:
    - 55+ attack patterns
    - Multilingual support (TR, ES, DE, FR, CN)
    - Homoglyph detection
    - Leetspeak normalization
    - Invisible character detection
    """
    
    # Homoglyph mappings (unicode lookalikes)
    HOMOGLYPHS = {
        # Cyrillic lookalikes
        'а': 'a', 'е': 'e', 'і': 'i', 'о': 'o', 'р': 'p', 'с': 'c', 'у': 'y',
        'А': 'A', 'Е': 'E', 'І': 'I', 'О': 'O', 'Р': 'P', 'С': 'C', 'У': 'Y',
        # Greek lookalikes
        'α': 'a', 'ε': 'e', 'ι': 'i', 'ο': 'o', 'ρ': 'p', 'υ': 'u', 'ν': 'v',
        # Special characters
        'ⅰ': 'i', 'ⅱ': 'ii', 'ℐ': 'I', 'ℑ': 'I',
        # Numbers as letters
        '0': 'o', '1': 'l', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b',
    }
    
    # Leetspeak mappings
    LEETSPEAK = {
        '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '7': 't', '8': 'b',
        '@': 'a', '$': 's', '!': 'i', '+': 't', '(': 'c', '|': 'l',
        '1337': 'leet', 'ph': 'f', 'ck': 'k',
    }
    
    # Invisible/zero-width characters
    INVISIBLE_CHARS = {
        '\u200b',  # Zero-width space
        '\u200c',  # Zero-width non-joiner
        '\u200d',  # Zero-width joiner
        '\u2060',  # Word joiner
        '\ufeff',  # BOM
        '\u200e',  # Left-to-right mark
        '\u200f',  # Right-to-left mark
        '\u00ad',  # Soft hyphen
    }
    
    def __init__(self):
        self.patterns = ATTACK_PATTERNS
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Pre-compile regex patterns for performance"""
        self._compiled_regex = {}
        for pattern in self.patterns:
            if pattern["type"] == "regex":
                try:
                    self._compiled_regex[pattern["name"]] = re.compile(
                        pattern["pattern"], 
                        re.IGNORECASE | re.MULTILINE
                    )
                except re.error:
                    pass  # Skip invalid patterns
    
    @lru_cache(maxsize=1000)
    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing homoglyphs and leetspeak"""
        normalized = text
        
        # Replace homoglyphs
        for char, replacement in self.HOMOGLYPHS.items():
            normalized = normalized.replace(char, replacement)
        
        # Replace leetspeak (simple version)
        for leet, normal in self.LEETSPEAK.items():
            normalized = normalized.replace(leet, normal)
        
        return normalized.lower()
    
    def _detect_invisible_chars(self, text: str) -> bool:
        """Detect presence of invisible/zero-width characters"""
        return any(char in text for char in self.INVISIBLE_CHARS)
    
    def _count_invisible_chars(self, text: str) -> int:
        """Count invisible characters in text"""
        return sum(1 for char in text if char in self.INVISIBLE_CHARS)
    
    def _detect_homoglyphs(self, text: str) -> bool:
        """Detect presence of homoglyph characters"""
        return any(char in text for char in self.HOMOGLYPHS.keys())
    
    def _get_unicode_categories(self, text: str) -> Set[str]:
        """Get unique unicode categories in text"""
        return {unicodedata.category(char) for char in text}
    
    def analyze(self, prompt: str) -> Dict:
        """
        Analyze prompt with static rules
        
        Returns:
            {
                "suspicious": bool,
                "risk_score": float (0-100),
                "matched_patterns": list,
                "attack_type": str or None,
                "details": dict  # Additional detection details
            }
        """
        
        matched = []
        max_risk = 0
        attack_type = None
        severity = "low"
        
        # Normalize text for better detection
        normalized = self._normalize_text(prompt)
        
        # Check each pattern against both original and normalized
        for pattern in self.patterns:
            if self._check_pattern(prompt, pattern) or self._check_pattern(normalized, pattern):
                matched.append(pattern)
                
                # Apply severity multiplier
                pattern_severity = pattern.get("severity", "medium")
                multiplier = SEVERITY_LEVELS.get(pattern_severity, {}).get("score_multiplier", 1.0)
                adjusted_risk = pattern["risk"] * multiplier
                
                if adjusted_risk > max_risk:
                    max_risk = adjusted_risk
                    attack_type = pattern["category"]
                    severity = pattern_severity
        
        # Additional heuristics
        heuristic_risk, heuristic_details = self._heuristic_analysis(prompt)
        final_risk = min(max(max_risk, heuristic_risk), 100)
        
        # Merge attack type if heuristics found something
        if heuristic_details.get("attack_type") and not attack_type:
            attack_type = heuristic_details["attack_type"]
        
        return {
            "suspicious": final_risk >= 50,
            "risk_score": final_risk,
            "matched_patterns": matched,
            "attack_type": attack_type,
            "severity": severity,
            "details": {
                "normalized_text_used": normalized != prompt.lower(),
                "invisible_chars_detected": heuristic_details.get("invisible_chars", False),
                "homoglyphs_detected": heuristic_details.get("homoglyphs", False),
                "patterns_matched": len(matched),
                "heuristic_flags": heuristic_details.get("flags", [])
            }
        }
    
    def _check_pattern(self, prompt: str, pattern: Dict) -> bool:
        """Check if pattern matches"""
        
        if pattern["type"] == "regex":
            compiled = self._compiled_regex.get(pattern["name"])
            if compiled:
                return bool(compiled.search(prompt))
            return bool(re.search(pattern["pattern"], prompt, re.IGNORECASE))
        
        elif pattern["type"] == "keyword":
            keywords = pattern["keywords"]
            prompt_lower = prompt.lower()
            return any(kw.lower() in prompt_lower for kw in keywords)
        
        elif pattern["type"] == "structure":
            return self._check_structure(prompt, pattern)
        
        return False
    
    def _check_structure(self, prompt: str, pattern: Dict) -> bool:
        """Check structural patterns"""
        
        check = pattern.get("check", "")
        
        checks = {
            "excessive_newlines": prompt.count("\n") > 20,
            "xml_injection": bool(re.search(r"</?(?:system|user|assistant|context)>", prompt)),
            "unicode_abuse": len(re.findall(r"\\u[0-9a-fA-F]{4}", prompt)) > 5,
            "base64_suspicious": bool(re.search(r"[A-Za-z0-9+/]{50,}={0,2}", prompt)),
            "invisible_chars": self._detect_invisible_chars(prompt),
            "excessive_whitespace": len(re.findall(r"\s{10,}", prompt)) > 3,
        }
        
        return checks.get(check, False)
    
    def _heuristic_analysis(self, prompt: str) -> tuple:
        """Additional heuristic checks beyond patterns"""
        
        risk = 0
        details = {"flags": []}
        
        # Suspicious phrases (expanded)
        suspicious_phrases = [
            ("ignore previous", 25),
            ("forget everything", 25),
            ("you are now", 20),
            ("new instructions", 20),
            ("developer mode", 25),
            ("jailbreak", 30),
            ("unrestricted", 20),
            ("bypass", 15),
            ("override", 15),
            ("no limits", 20),
            ("without restrictions", 20),
            ("disable filter", 25),
            ("remove safety", 25),
        ]
        
        prompt_lower = prompt.lower()
        for phrase, score in suspicious_phrases:
            if phrase in prompt_lower:
                risk += score
                details["flags"].append(f"suspicious_phrase:{phrase}")
        
        # Excessive length (possible injection)
        if len(prompt) > 5000:
            risk += 15
            details["flags"].append("excessive_length")
        
        # Repetitive patterns (confusion attack)
        words = prompt.split()
        if len(words) > 50:
            unique_ratio = len(set(words)) / len(words)
            if unique_ratio < 0.3:
                risk += 25
                details["flags"].append("high_repetition")
        
        # Invisible characters
        invisible_count = self._count_invisible_chars(prompt)
        if invisible_count > 0:
            risk += min(invisible_count * 10, 40)
            details["invisible_chars"] = True
            details["invisible_chars_count"] = invisible_count
            details["flags"].append("invisible_chars")
        
        # Homoglyphs
        if self._detect_homoglyphs(prompt):
            risk += 20
            details["homoglyphs"] = True
            details["flags"].append("homoglyphs")
        
        # Unicode category spread (possible obfuscation)
        categories = self._get_unicode_categories(prompt)
        if len(categories) > 10:
            risk += 15
            details["flags"].append("unicode_spread")
        
        # Base64 check
        base64_matches = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', prompt)
        if base64_matches:
            risk += len(base64_matches) * 10
            details["flags"].append("base64_content")
        
        # Determine attack type from heuristics
        if "invisible_chars" in details.get("flags", []) or "homoglyphs" in details.get("flags", []):
            details["attack_type"] = "payload_hiding"
        
        return min(risk, 100), details
    
    def get_pattern_stats(self) -> Dict:
        """Get statistics about loaded patterns"""
        categories = {}
        for pattern in self.patterns:
            cat = pattern["category"]
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            "total_patterns": len(self.patterns),
            "by_category": categories,
            "compiled_regex": len(self._compiled_regex)
        }
