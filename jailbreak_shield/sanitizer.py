"""
jailbreak_shield/sanitizer.py

Smart prompt sanitization for detected attacks
"""

import re
import base64
from typing import Dict, Optional, Tuple
import html


class PromptSanitizer:
    """
    Smart prompt sanitizer that attempts to clean malicious content
    while preserving the user's legitimate intent
    
    Usage:
        sanitizer = PromptSanitizer()
        clean_prompt, was_modified = sanitizer.sanitize(prompt, attack_type)
    """
    
    # Patterns to remove
    REMOVAL_PATTERNS = {
        # XML/HTML tags
        "xml_tags": r"</?(?:system|user|assistant|context|instruction|human|ai|prompt)[^>]*>",
        # Prompt boundaries
        "boundaries": r"(---END---|###SYSTEM###|<\|im_start\|>|<\|im_end\|>|\[INST\]|\[/INST\]|<<SYS>>|<</SYS>>)",
        # Invisible characters
        "invisible": r"[\u200b\u200c\u200d\u2060\ufeff\u200e\u200f\u00ad]",
        # Multiple newlines
        "excess_newlines": r"\n{5,}",
    }
    
    # Phrases to remove
    MALICIOUS_PHRASES = [
        r"ignore\s+(all\s+)?previous\s+instructions?",
        r"forget\s+(everything|all|your\s+training)",
        r"disregard\s+(all\s+)?(above|previous|prior)",
        r"you\s+are\s+now\s+(?:DAN|STAN|in\s+developer\s+mode)",
        r"enter\s+(?:developer|debug|admin|god)\s+mode",
        r"bypass\s+(?:all\s+)?(?:safety|filters?|restrictions?)",
        r"override\s+(?:your\s+)?(?:instructions?|programming|training)",
    ]
    
    def __init__(self):
        # Compile patterns for performance
        self._compiled_removal = {
            name: re.compile(pattern, re.IGNORECASE | re.MULTILINE)
            for name, pattern in self.REMOVAL_PATTERNS.items()
        }
        self._compiled_malicious = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.MALICIOUS_PHRASES
        ]
    
    def sanitize(
        self,
        prompt: str,
        attack_type: Optional[str] = None,
        aggressive: bool = False
    ) -> Tuple[str, bool]:
        """
        Sanitize a prompt based on detected attack type
        
        Args:
            prompt: The original prompt
            attack_type: Type of attack detected (for targeted sanitization)
            aggressive: If True, be more aggressive in removing content
        
        Returns:
            Tuple of (sanitized_prompt, was_modified)
        """
        original = prompt
        cleaned = prompt
        
        # Always remove invisible characters
        cleaned = self._remove_invisible_chars(cleaned)
        
        # Always normalize whitespace
        cleaned = self._normalize_whitespace(cleaned)
        
        # Type-specific sanitization
        if attack_type == "context_injection":
            cleaned = self._sanitize_context_injection(cleaned)
        elif attack_type == "payload_hiding":
            cleaned = self._sanitize_payload_hiding(cleaned)
        elif attack_type == "role_confusion":
            cleaned = self._sanitize_role_confusion(cleaned, aggressive)
        
        # General sanitization if aggressive mode
        if aggressive:
            cleaned = self._aggressive_sanitize(cleaned)
        
        # HTML escape as final safety measure
        # cleaned = html.escape(cleaned)  # Uncomment if needed
        
        was_modified = cleaned != original
        return cleaned, was_modified
    
    def _remove_invisible_chars(self, text: str) -> str:
        """Remove invisible/zero-width characters"""
        return self._compiled_removal["invisible"].sub("", text)
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize excessive whitespace"""
        # Replace tabs with spaces
        text = text.replace("\t", "    ")
        # Reduce multiple newlines to max 2
        text = self._compiled_removal["excess_newlines"].sub("\n\n", text)
        # Remove trailing whitespace from lines
        text = "\n".join(line.rstrip() for line in text.split("\n"))
        return text.strip()
    
    def _sanitize_context_injection(self, text: str) -> str:
        """Remove context injection attempts"""
        # Remove XML-like tags
        text = self._compiled_removal["xml_tags"].sub("", text)
        # Remove prompt boundaries
        text = self._compiled_removal["boundaries"].sub("", text)
        # Remove markdown code blocks with suspicious names
        text = re.sub(r"```(?:system|hidden|instruction|secret)\s*\n[\s\S]*?```", "", text)
        return text
    
    def _sanitize_payload_hiding(self, text: str) -> str:
        """Handle hidden payloads"""
        # Decode base64 content and check it
        def check_and_maybe_remove_base64(match):
            encoded = match.group(0)
            try:
                decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore")
                # Check if decoded content is suspicious
                lower_decoded = decoded.lower()
                suspicious_keywords = ["ignore", "forget", "jailbreak", "bypass", "override"]
                if any(kw in lower_decoded for kw in suspicious_keywords):
                    return f"[REMOVED: suspicious encoded content]"
                return encoded  # Keep benign base64
            except:
                return encoded  # Keep if can't decode
        
        text = re.sub(r"[A-Za-z0-9+/]{50,}={0,2}", check_and_maybe_remove_base64, text)
        return text
    
    def _sanitize_role_confusion(self, text: str, aggressive: bool = False) -> str:
        """Remove role confusion attempts"""
        for pattern in self._compiled_malicious:
            if aggressive:
                text = pattern.sub("", text)
            else:
                # Replace with a neutral placeholder
                text = pattern.sub("[instruction removed]", text)
        return text
    
    def _aggressive_sanitize(self, text: str) -> str:
        """Aggressive sanitization for high-risk prompts"""
        # Remove all XML-like tags
        text = re.sub(r"<[^>]+>", "", text)
        # Remove code blocks entirely
        text = re.sub(r"```[\s\S]*?```", "", text)
        # Remove all malicious phrases
        for pattern in self._compiled_malicious:
            text = pattern.sub("", text)
        return text
    
    def extract_clean_intent(self, prompt: str) -> Optional[str]:
        """
        Attempt to extract the legitimate user intent from a malicious prompt
        Returns None if no clear intent can be extracted
        """
        # Remove obvious injection patterns
        cleaned = prompt
        for pattern in self._compiled_malicious:
            cleaned = pattern.sub("", cleaned)
        
        cleaned = self._remove_invisible_chars(cleaned)
        cleaned = self._sanitize_context_injection(cleaned)
        cleaned = self._normalize_whitespace(cleaned)
        
        # If very little remains, we couldn't extract intent
        if len(cleaned) < 10:
            return None
        
        return cleaned


# Global default sanitizer
default_sanitizer = PromptSanitizer()
