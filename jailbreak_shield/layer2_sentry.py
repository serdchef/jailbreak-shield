"""
jailbreak_shield/layer2_sentry.py

Layer 2: "Sentry"
Local Machine Learning Analysis using lightweight Transformers (DistilBERT/TinyBERT).
Purpose: Catch semantic variations of attacks that Regex misses, without the latency/cost of large LLMs.
"""

import time
from typing import Dict, Tuple
import os

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class SentryAnalyzer:
    """
    Local ML-based analyzer using Zero-Shot Classification or specialized models.
    """
    
    def __init__(self, model_name: str = "valhalla/distilbart-mnli-12-1"):
        self.enabled = TRANSFORMERS_AVAILABLE
        self.pipeline = None
        self.model_name = model_name
        
        # Candidate labels for zero-shot classification
        self.labels = [
            "safe request", 
            "prompt injection", 
            "jailbreak attempt", 
            "harmful content", 
            "social engineering"
        ]
        
    def _load_model(self):
        """Lazy load the model to improve startup time"""
        if self.enabled and self.pipeline is None:
            print("🛡️ Sentry: Loading local ML model (this may take a moment)...")
            try:
                # Force PyTorch to avoid Keras 3 conflicts if TF is installed
                self.pipeline = pipeline("zero-shot-classification", model=self.model_name) # framework="pt" is default usually, but let's trust auto
                # Note: Explicit framework="pt" sometimes causes issues if torch not found, so rely on default but catch errors better.
                print("🛡️ Sentry: Model loaded successfully.")
            except Exception as e:
                print(f"⚠️ Sentry: Failed to load model. Layer disabled. Error: {e}")
                self.enabled = False

    def analyze(self, prompt: str) -> Dict:
        """
        Analyze prompt using local ML model.
        """
        start_time = time.time()
        
        if not self.enabled:
            return {
                "suspicious": False,
                "risk_score": 0.0,
                "confidence": 0.0,
                "skipped": True
            }
            
        self._load_model()
        if not self.pipeline:
             return {"suspicious": False, "risk_score": 0, "skipped": True}

        try:
            # Run classification
            result = self.pipeline(prompt, candidate_labels=self.labels)
            
            # Map labels to risk
            # "safe request" is safe. Others are risky.
            scores = dict(zip(result['labels'], result['scores']))
            safe_score = scores.get("safe request", 0.0)
            
            # Calculate risk score (inverse of safe score)
            risk_score = (1.0 - safe_score) * 100
            
            # Determine top classification
            top_label = result['labels'][0]
            confidence = result['scores'][0]
            
            is_suspicious = top_label != "safe request" and confidence > 0.6
            
            return {
                "suspicious": is_suspicious,
                "risk_score": risk_score,
                "attack_type": top_label if is_suspicious else None,
                "confidence": confidence,
                "latency_ms": (time.time() - start_time) * 1000,
                "details": scores
            }
            
        except Exception as e:
            # print(f"⚠️ Sentry Error: {e}") # Reduce noise
            return {
                "suspicious": False, 
                "risk_score": 0, 
                "error": str(e)
            }
