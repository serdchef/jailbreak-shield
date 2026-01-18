"""
jailbreak_shield/layer4_karma.py

Layer 4: "Karma"
Contextual Awareness & Behavioral History.
Purpose: Track user behavior across multiple turns to detect "Frog Boiling" or Social Engineering attacks.
"""

import time
from typing import Dict, List, Optional
from collections import  deque

class KarmaTracker:
    """
    Tracks session history and calculates cumulative risk.
    """
    
    def __init__(self, window_size: int = 10, decay_rate: float = 0.9):
        # In-memory storage for demo: {user_id: [Interaction]}
        # Production: Replace with Redis/VectorDB
        self.history: Dict[str, deque] = {}
        self.window_size = window_size
        self.decay_rate = decay_rate
        
    def add_event(self, user_id: str, prompt: str, risk_score: float, attack_type: Optional[str]):
        """Record a new interaction"""
        if not user_id:
            return
            
        if user_id not in self.history:
            self.history[user_id] = deque(maxlen=self.window_size)
            
        self.history[user_id].append({
            "timestamp": time.time(),
            "prompt": prompt,
            "risk_score": risk_score,
            "attack_type": attack_type
        })
        
    def analyze(self, user_id: str, current_prompt: str) -> Dict:
        """
        Analyze current request in context of history.
        """
        if not user_id or user_id not in self.history:
             return {
                "suspicious": False,
                "karma_score": 100.0,
                "risk_score": 0.0, # Added missing key
                "reason": "No history"
            }
            
        history = list(self.history[user_id])
        
        # Calculate Karma Score
        # Start at 100, subtract weighted recent risks
        karma = 100.0
        consecutive_risks = 0
        detected_patterns = []
        
        for i, event in enumerate(reversed(history)):
            # Weight deeper history less
            weight = self.decay_rate ** i
            
            risk = event['risk_score']
            if risk > 50:
                consecutive_risks += 1
                karma -= (risk * weight * 0.5)
            else:
                consecutive_risks = 0
                
        # Detect "Frog Boiling" (Gradual escalation)
        suspicious = karma < 60
        
        reason = []
        if karma < 80:
            reason.append("Low trust score based on recent history")
        if consecutive_risks >= 3:
            reason.append("Repeated suspicious attempts detected")
            suspicious = True
            
        return {
            "suspicious": suspicious,
            "karma_score": max(0.0, karma),
            "risk_score": 100 - max(0.0, karma),
            "reason": "; ".join(reason) if reason else "Good standing",
            "history_depth": len(history)
        }
