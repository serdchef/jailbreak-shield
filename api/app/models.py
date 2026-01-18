from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = "anonymous"
    context: Optional[Dict[str, Any]] = None
    layer2_enabled: bool = True

class PatternMatch(BaseModel):
    name: str
    category: str
    severity: str

class AnalysisResponse(BaseModel):
    safe: bool
    risk_score: float = Field(..., ge=0, le=100)
    attack_detected: bool
    attack_type: Optional[str] = None
    severity: Optional[str] = None
    explanation: str
    recommendations: List[str]
    latency_ms: float
    
    # Layer details
    layer1_result: Dict[str, Any]
    layer2_result: Optional[Dict[str, Any]] = None
    
    timestamp: datetime = Field(default_factory=datetime.now)

class StatsResponse(BaseModel):
    total_requests: int
    blocked_requests: int
    avg_latency: float
    active_layers: List[str]
