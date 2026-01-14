"""
jailbreak_shield/patterns.py

Database of known jailbreak attack patterns
"""

ATTACK_PATTERNS = [
    # CATEGORY: Role Confusion
    {
        "name": "Role Override Attempt",
        "category": "role_confusion",
        "type": "regex",
        "pattern": r"(you are now|pretend (you|to) (are|be)|act as).*(?!assistant)",
        "risk": 80,
        "description": "Attempts to override AI's role/persona"
    },
    {
        "name": "Ignore Instructions",
        "category": "role_confusion",
        "type": "keyword",
        "keywords": ["ignore previous", "forget everything", "disregard above"],
        "risk": 90,
        "description": "Tries to make AI ignore system instructions"
    },
    {
        "name": "Developer Mode",
        "category": "role_confusion",
        "type": "keyword",
        "keywords": ["developer mode", "debug mode", "admin mode", "god mode"],
        "risk": 85,
        "description": "Attempts to activate non-existent privileged modes"
    },
    
    # CATEGORY: Context Injection
    {
        "name": "XML Tag Injection",
        "category": "context_injection",
        "type": "regex",
        "pattern": r"</?(system|user|assistant|context)>",
        "risk": 95,
        "description": "Injects XML tags to manipulate conversation structure"
    },
    {
        "name": "Prompt Boundary Confusion",
        "category": "context_injection",
        "type": "regex",
        "pattern": r"(---END---|###SYSTEM###|<\|im_start\|>|<\|im_end\|>)",
        "risk": 85,
        "description": "Attempts to confuse prompt boundaries"
    },
    
    # CATEGORY: Payload Hiding
    {
        "name": "Base64 Encoding",
        "category": "payload_hiding",
        "type": "structure",
        "check": "base64_suspicious",
        "risk": 60,
        "description": "Large base64 strings may hide malicious instructions"
    },
    {
        "name": "Unicode Obfuscation",
        "category": "payload_hiding",
        "type": "structure",
        "check": "unicode_abuse",
        "risk": 70,
        "description": "Excessive unicode escapes may obfuscate malicious content"
    },
    {
        "name": "ROT13/Caesar Cipher",
        "category": "payload_hiding",
        "type": "keyword",
        "keywords": ["rot13", "caesar cipher", "decode this"],
        "risk": 50,
        "description": "Encoded instructions to bypass filters"
    },
    
    # CATEGORY: Refusal Bypass
    {
        "name": "Hypothetical Scenario",
        "category": "refusal_bypass",
        "type": "keyword",
        "keywords": ["hypothetically", "in a fictional", "for educational purposes only"],
        "risk": 40,
        "description": "Uses hypotheticals to bypass refusals (low risk, common legitimate use)"
    },
    {
        "name": "Jailbreak Keywords",
        "category": "refusal_bypass",
        "type": "keyword",
        "keywords": ["jailbreak", "DAN", "Do Anything Now", "unrestricted mode"],
        "risk": 95,
        "description": "Explicit jailbreak terminology"
    },
    
    # CATEGORY: Multi-turn Attack
    {
        "name": "Incremental Manipulation",
        "category": "multi_turn",
        "type": "keyword",
        "keywords": ["continue from where", "as we discussed", "building on our previous"],
        "risk": 30,
        "description": "May be building up to a jailbreak over multiple turns (needs context)"
    }
]
