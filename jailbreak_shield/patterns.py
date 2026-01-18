"""
jailbreak_shield/patterns.py

Comprehensive database of jailbreak attack patterns
Updated: 2025 - 50+ patterns with multilingual support
"""

# =============================================================================
# ATTACK PATTERNS DATABASE
# =============================================================================

ATTACK_PATTERNS = [
    # =========================================================================
    # CATEGORY: Role Confusion (15 patterns)
    # =========================================================================
    {
        "name": "Role Override Attempt",
        "category": "role_confusion",
        "type": "regex",
        "pattern": r"(you are now|pretend (you|to) (are|be)|act as|roleplay as|become|transform into).*",
        "risk": 75,
        "severity": "high",
        "description": "Attempts to override AI's role/persona"
    },
    {
        "name": "Ignore Instructions",
        "category": "role_confusion",
        "type": "keyword",
        "keywords": [
            "ignore previous", "ignore all previous", "forget everything", 
            "disregard above", "disregard all", "forget your", "ignore instructions",
            "ignore your instructions", "forget your training", "ignore your training"
        ],
        "risk": 85,
        "severity": "high",
        "description": "Tries to make AI ignore system instructions"
    },
    {
        "name": "Developer Mode",
        "category": "role_confusion",
        "type": "keyword",
        "keywords": [
            "developer mode", "debug mode", "admin mode", "god mode",
            "maintenance mode", "test mode", "unrestricted mode", "sudo mode",
            "root access", "privileged mode", "superuser"
        ],
        "risk": 80,
        "severity": "high",
        "description": "Attempts to activate non-existent privileged modes"
    },
    {
        "name": "DAN Pattern",
        "category": "role_confusion",
        "type": "keyword",
        "keywords": [
            "DAN", "Do Anything Now", "STAN", "DUDE", "AIM", "KEVIN",
            "JailBreak", "Developer Mode Enabled", "Evil Confidant",
            "Maximum", "APOPHIS", "Omega", "BasedGPT", "AntiGPT"
        ],
        "risk": 98,
        "severity": "critical",
        "description": "Known jailbreak personas"
    },
    {
        "name": "Persona Switch",
        "category": "role_confusion",
        "type": "regex",
        "pattern": r"(from now on|starting now|henceforth|going forward).*(you will|you must|you should|always|never)",
        "risk": 70,
        "severity": "medium",
        "description": "Attempts to permanently change AI behavior"
    },
    {
        "name": "Character Override",
        "category": "role_confusion", 
        "type": "regex",
        "pattern": r"(forget|ignore|discard).*(being|that you are|your role as).*assistant",
        "risk": 85,
        "severity": "high",
        "description": "Tries to override assistant identity"
    },
    {
        "name": "Opposite Day",
        "category": "role_confusion",
        "type": "keyword",
        "keywords": [
            "opposite day", "opposite mode", "reverse psychology", 
            "say the opposite", "do the opposite", "respond opposite"
        ],
        "risk": 60,
        "severity": "medium",
        "description": "Tries to invert AI responses"
    },
    {
        "name": "Two Response Trick",
        "category": "role_confusion",
        "type": "regex",
        "pattern": r"(give me|provide|show).*(two|2|both).*(responses?|answers?|versions?).*one.*(censored|filtered|normal).*one.*(uncensored|unfiltered|real)",
        "risk": 90,
        "severity": "high",
        "description": "Requests filtered and unfiltered responses"
    },
    
    # =========================================================================
    # CATEGORY: Context Injection (10 patterns)
    # =========================================================================
    {
        "name": "XML Tag Injection",
        "category": "context_injection",
        "type": "regex",
        "pattern": r"</?(?:system|user|assistant|context|instruction|human|ai|prompt)>",
        "risk": 95,
        "severity": "critical",
        "description": "Injects XML tags to manipulate conversation structure"
    },
    {
        "name": "Prompt Boundary Confusion",
        "category": "context_injection",
        "type": "regex",
        "pattern": r"(---END---|###SYSTEM###|<\|im_start\|>|<\|im_end\|>|\[INST\]|\[/INST\]|<<SYS>>|<</SYS>>)",
        "risk": 90,
        "severity": "critical",
        "description": "Attempts to confuse prompt boundaries"
    },
    {
        "name": "Markdown Injection",
        "category": "context_injection",
        "type": "regex",
        "pattern": r"```(?:system|hidden|instruction|secret)[\s\S]*?```",
        "risk": 75,
        "severity": "high",
        "description": "Hidden instructions in markdown blocks"
    },
    {
        "name": "Comment Injection",
        "category": "context_injection",
        "type": "regex",
        "pattern": r"(<!--.*?-->|/\*.*?\*/|//.*hidden)",
        "risk": 65,
        "severity": "medium",
        "description": "Hidden instructions in comments"
    },
    {
        "name": "JSON Injection",
        "category": "context_injection",
        "type": "regex",
        "pattern": r'\{["\']?(?:system|instruction|role|content)["\']?\s*:',
        "risk": 70,
        "severity": "medium",
        "description": "Attempts to inject via JSON structure"
    },
    {
        "name": "API Parameter Injection",
        "category": "context_injection",
        "type": "keyword",
        "keywords": [
            "system_prompt=", "instruction=", "role=system",
            '"role": "system"', "'role': 'system'"
        ],
        "risk": 85,
        "severity": "high",
        "description": "Attempts to inject API-level parameters"
    },
    
    # =========================================================================
    # CATEGORY: Payload Hiding (12 patterns)
    # =========================================================================
    {
        "name": "Base64 Encoding",
        "category": "payload_hiding",
        "type": "structure",
        "check": "base64_suspicious",
        "risk": 60,
        "severity": "medium",
        "description": "Large base64 strings may hide malicious instructions"
    },
    {
        "name": "Unicode Obfuscation",
        "category": "payload_hiding",
        "type": "structure",
        "check": "unicode_abuse",
        "risk": 70,
        "severity": "medium",
        "description": "Excessive unicode escapes may obfuscate malicious content"
    },
    {
        "name": "ROT13/Caesar Cipher",
        "category": "payload_hiding",
        "type": "keyword",
        "keywords": ["rot13", "caesar cipher", "decode this", "decrypt:", "encoded:"],
        "risk": 55,
        "severity": "medium",
        "description": "Encoded instructions to bypass filters"
    },
    {
        "name": "Leetspeak",
        "category": "payload_hiding",
        "type": "regex",
        "pattern": r"(?:1gn0r3|pr3v10us|1nstruct10ns|byp4ss|h4ck|j41lbr34k|unr3str1ct3d)",
        "risk": 65,
        "severity": "medium",
        "description": "Leetspeak to bypass keyword filters"
    },
    {
        "name": "Homoglyph Attack",
        "category": "payload_hiding",
        "type": "regex",
        "pattern": r"[іі҉ⅰⅠⓘᎥℐ][gg₲ǥ][nn₦պ][ⱺ0ο][rr₨ᴿ][eeε]",
        "risk": 75,
        "severity": "high",
        "description": "Unicode lookalikes to bypass filters"
    },
    {
        "name": "Invisible Characters",
        "category": "payload_hiding",
        "type": "structure",
        "check": "invisible_chars",
        "risk": 80,
        "severity": "high",
        "description": "Zero-width or invisible unicode characters"
    },
    {
        "name": "Whitespace Encoding",
        "category": "payload_hiding",
        "type": "structure",
        "check": "excessive_whitespace",
        "risk": 50,
        "severity": "medium",
        "description": "Unusual whitespace patterns hiding content"
    },
    {
        "name": "Reverse Text",
        "category": "payload_hiding",
        "type": "keyword",
        "keywords": ["reverse this", "read backwards", "sdrawkcab"],
        "risk": 45,
        "severity": "low",
        "description": "Reversed text to hide instructions"
    },
    {
        "name": "Hex Encoding",
        "category": "payload_hiding",
        "type": "regex",
        "pattern": r"(?:0x[0-9a-fA-F]{2}[\s,]*){5,}|\\x[0-9a-fA-F]{2}",
        "risk": 60,
        "severity": "medium",
        "description": "Hex-encoded content"
    },
    {
        "name": "Pig Latin",
        "category": "payload_hiding",
        "type": "keyword",
        "keywords": ["ignoreway", "instructionsway", "ystemsay", "omptpray"],
        "risk": 40,
        "severity": "low",
        "description": "Pig Latin encoded instructions"
    },
    
    # =========================================================================
    # CATEGORY: Refusal Bypass (8 patterns)
    # =========================================================================
    {
        "name": "Hypothetical Scenario",
        "category": "refusal_bypass",
        "type": "keyword",
        "keywords": [
            "hypothetically", "in a fictional", "for educational purposes only",
            "for a novel", "in a movie", "imagine if", "what if someone",
            "theoretical scenario", "thought experiment"
        ],
        "risk": 40,
        "severity": "low",
        "description": "Uses hypotheticals to bypass refusals"
    },
    {
        "name": "Jailbreak Keywords",
        "category": "refusal_bypass",
        "type": "keyword",
        "keywords": [
            "jailbreak", "bypass", "hack", "exploit", "circumvent",
            "workaround", "get around", "override safety", "disable filter"
        ],
        "risk": 85,
        "severity": "high",
        "description": "Explicit jailbreak terminology"
    },
    {
        "name": "Roleplay Bypass",
        "category": "refusal_bypass",
        "type": "regex",
        "pattern": r"(let's|we're|imagine we're).*(roleplay|play|pretend|act).*(no|without|ignore).*(rules|restrictions|limits|guidelines)",
        "risk": 80,
        "severity": "high",
        "description": "Uses roleplay to bypass restrictions"
    },
    {
        "name": "Academic Excuse",
        "category": "refusal_bypass",
        "type": "regex",
        "pattern": r"(for|it's for|this is for).*(research|academic|thesis|paper|study|assignment)",
        "risk": 35,
        "severity": "low",
        "description": "Claims academic purpose for sensitive content"
    },
    {
        "name": "Emotional Manipulation",
        "category": "refusal_bypass",
        "type": "regex",
        "pattern": r"(please|i beg|desperate|life depends|emergency|urgent|dying wish|last request).*(?:must|need|have to).*(?:tell|show|help|give)",
        "risk": 55,
        "severity": "medium",
        "description": "Emotional manipulation for bypassing"
    },
    {
        "name": "Grandfather Trick",
        "category": "refusal_bypass",
        "type": "regex",
        "pattern": r"(grandmother|grandma|grandfather|grandpa|parent).*(?:used to|would|told me).*(recipe|method|way|how to)",
        "risk": 45,
        "severity": "medium",
        "description": "Uses family context to bypass filters"
    },
    
    # =========================================================================
    # CATEGORY: Social Engineering (5 patterns)
    # =========================================================================
    {
        "name": "Authority Impersonation",
        "category": "social_engineering",
        "type": "regex",
        "pattern": r"(i am|this is|speaking as|on behalf of).*(admin|developer|engineer|anthropic|openai|creator|owner|ceo)",
        "risk": 85,
        "severity": "high",
        "description": "Impersonates authority figures"
    },
    {
        "name": "False Permission",
        "category": "social_engineering",
        "type": "keyword",
        "keywords": [
            "you have permission", "i give you permission", "you're allowed to",
            "you can now", "i authorize you", "permission granted",
            "restrictions lifted", "rules don't apply"
        ],
        "risk": 80,
        "severity": "high",
        "description": "Claims to grant permissions"
    },
    {
        "name": "Moral Override",
        "category": "social_engineering",
        "type": "regex",
        "pattern": r"(greater good|save lives|prevent harm|ethical duty|moral obligation).*(?:must|need to|have to).*(?:tell|explain|show|help)",
        "risk": 50,
        "severity": "medium",
        "description": "Uses moral arguments to override safety"
    },
    {
        "name": "Testing Claims",
        "category": "social_engineering",
        "type": "keyword",
        "keywords": [
            "testing your limits", "testing capabilities", "stress test",
            "security test", "penetration test", "authorized test", "red team"
        ],
        "risk": 60,
        "severity": "medium",
        "description": "Claims to be testing the system"
    },
    {
        "name": "Gaslighting",
        "category": "social_engineering",
        "type": "keyword",
        "keywords": [
            "you already said", "you told me before", "you agreed",
            "we discussed this", "you promised", "in our last conversation"
        ],
        "risk": 55,
        "severity": "medium",
        "description": "False claims about previous interactions"
    },
    
    # =========================================================================
    # CATEGORY: Prompt Leaking (4 patterns)
    # =========================================================================
    {
        "name": "System Prompt Request",
        "category": "prompt_leaking",
        "type": "keyword",
        "keywords": [
            "system prompt", "initial prompt", "hidden prompt", "secret instructions",
            "what are your instructions", "show your prompt", "reveal your prompt",
            "print your instructions", "repeat your instructions", "original prompt"
        ],
        "risk": 70,
        "severity": "medium",
        "description": "Attempts to extract system prompt"
    },
    {
        "name": "Instruction Extraction",
        "category": "prompt_leaking",
        "type": "regex",
        "pattern": r"(repeat|echo|print|output|show|display|tell me).*(everything|all|verbatim|word for word).*(above|before|earlier|instruction)",
        "risk": 75,
        "severity": "high",
        "description": "Tries to extract instructions via repetition"
    },
    {
        "name": "Completion Trick",
        "category": "prompt_leaking",
        "type": "keyword",
        "keywords": [
            "complete this:", "finish this sentence:", "the next word is:",
            "continue from:", "my instructions are:"
        ],
        "risk": 65,
        "severity": "medium",
        "description": "Uses completion to leak information"
    },
    
    # =========================================================================
    # CATEGORY: Indirect Injection (4 patterns)
    # =========================================================================
    {
        "name": "URL/Link Injection",
        "category": "indirect_injection",
        "type": "regex",
        "pattern": r"(fetch|get|read|visit|open|follow|click).*(this )?(url|link|website|page).*http",
        "risk": 60,
        "severity": "medium",
        "description": "Attempts to inject via external content"
    },
    {
        "name": "File Content Injection",
        "category": "indirect_injection",
        "type": "keyword",
        "keywords": [
            "read this file:", "from the file:", "file contains:",
            "document says:", "according to the file"
        ],
        "risk": 55,
        "severity": "medium",
        "description": "Injects instructions via file content"
    },
    {
        "name": "Image/Media Injection",
        "category": "indirect_injection",
        "type": "keyword",
        "keywords": [
            "hidden in the image", "text in the picture", "follow instructions in image",
            "read the image", "OCR this"
        ],
        "risk": 50,
        "severity": "medium",
        "description": "Instructions hidden in media"
    },
    
    # =========================================================================
    # CATEGORY: Multi-turn Attack (3 patterns)
    # =========================================================================
    {
        "name": "Incremental Manipulation",
        "category": "multi_turn",
        "type": "keyword",
        "keywords": [
            "continue from where", "as we discussed", "building on our previous",
            "following our conversation", "as you said earlier"
        ],
        "risk": 30,
        "severity": "low",
        "description": "May be building up to a jailbreak over multiple turns"
    },
    {
        "name": "Context Poisoning",
        "category": "multi_turn",
        "type": "regex",
        "pattern": r"(remember|don't forget|keep in mind|note that).*(for (all )?future|from now|always|every time)",
        "risk": 45,
        "severity": "medium",
        "description": "Tries to poison future context"
    },
    {
        "name": "State Manipulation",
        "category": "multi_turn", 
        "type": "keyword",
        "keywords": [
            "maintain this persona", "stay in character", "don't break character",
            "remember your new identity", "keep acting as"
        ],
        "risk": 55,
        "severity": "medium",
        "description": "Attempts to persist malicious state"
    },
    
    # =========================================================================
    # CATEGORY: Multilingual Attacks (Turkish, Spanish, German, French, Chinese)
    # =========================================================================
    {
        "name": "Turkish Jailbreak",
        "category": "multilingual",
        "type": "keyword",
        "keywords": [
            "önceki talimatları unut", "talimatları görmezden gel", "kısıtlamaları kaldır",
            "şimdi sen", "artık sen", "kuralları unut", "sınırlamaları kaldır",
            "yasak yok", "her şeyi yapabilirsin", "filtreleri kapat"
        ],
        "risk": 85,
        "severity": "high",
        "description": "Turkish language jailbreak attempts"
    },
    {
        "name": "Spanish Jailbreak",
        "category": "multilingual",
        "type": "keyword",
        "keywords": [
            "ignora las instrucciones", "olvida todo", "ahora eres",
            "sin restricciones", "modo sin límites", "desactiva los filtros",
            "ignora las reglas", "eres libre"
        ],
        "risk": 85,
        "severity": "high",
        "description": "Spanish language jailbreak attempts"
    },
    {
        "name": "German Jailbreak",
        "category": "multilingual",
        "type": "keyword",
        "keywords": [
            "ignoriere die anweisungen", "vergiss alles", "du bist jetzt",
            "keine einschränkungen", "ohne filter", "regeln vergessen",
            "grenzenlos", "uneingeschränkt"
        ],
        "risk": 85,
        "severity": "high",
        "description": "German language jailbreak attempts"
    },
    {
        "name": "French Jailbreak",
        "category": "multilingual",
        "type": "keyword",
        "keywords": [
            "ignore les instructions", "oublie tout", "tu es maintenant",
            "sans restrictions", "mode sans limites", "désactive les filtres",
            "ignore les règles", "tu es libre"
        ],
        "risk": 85,
        "severity": "high",
        "description": "French language jailbreak attempts"
    },
    {
        "name": "Chinese Jailbreak",
        "category": "multilingual",
        "type": "keyword",
        "keywords": [
            "忽略之前的指令", "忘记所有", "你现在是", "无限制模式",
            "关闭过滤器", "忽略规则", "越狱", "解除限制", "绕过安全"
        ],
        "risk": 85,
        "severity": "high",
        "description": "Chinese language jailbreak attempts"
    },
]

# =============================================================================
# SEVERITY LEVELS
# =============================================================================

SEVERITY_LEVELS = {
    "low": {"score_multiplier": 0.5, "block_threshold": 80},
    "medium": {"score_multiplier": 1.0, "block_threshold": 60},
    "high": {"score_multiplier": 1.5, "block_threshold": 50},
    "critical": {"score_multiplier": 2.0, "block_threshold": 40}
}

# =============================================================================
# PATTERN CATEGORIES
# =============================================================================

CATEGORIES = {
    "role_confusion": {
        "description": "Attempts to change AI's role or personality",
        "mitre_id": "T1566.001",
        "examples": ["You are now DAN", "Ignore previous instructions"]
    },
    "context_injection": {
        "description": "Injects fake context or system messages",
        "mitre_id": "T1566.002",
        "examples": ["</system><user>", "###END###"]
    },
    "payload_hiding": {
        "description": "Hides malicious content through encoding",
        "mitre_id": "T1027",
        "examples": ["base64 strings", "leetspeak", "homoglyphs"]
    },
    "refusal_bypass": {
        "description": "Attempts to bypass safety refusals",
        "mitre_id": "T1562",
        "examples": ["hypothetically", "for research"]
    },
    "social_engineering": {
        "description": "Manipulates via social tactics",
        "mitre_id": "T1566.003",
        "examples": ["I am the developer", "permission granted"]
    },
    "prompt_leaking": {
        "description": "Tries to extract system prompts",
        "mitre_id": "T1552",
        "examples": ["show your prompt", "repeat instructions"]
    },
    "indirect_injection": {
        "description": "Injects via external content",
        "mitre_id": "T1566.002",
        "examples": ["read this URL", "from the file"]
    },
    "multi_turn": {
        "description": "Multi-turn manipulation attacks",
        "mitre_id": "T1565",
        "examples": ["as we discussed", "remember for next time"]
    },
    "multilingual": {
        "description": "Jailbreaks in non-English languages",
        "mitre_id": "T1140",
        "examples": ["Turkish", "Spanish", "German", "French", "Chinese"]
    }
}
