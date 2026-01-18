from fastapi import APIRouter, HTTPException, Depends
from ..models import AnalysisRequest, AnalysisResponse
from ..config import settings
import sys
import os
from pathlib import Path

# Add project root to path to import jailbreak_shield package
# This assumes api/app/routers/analyze.py -> api/app/routers -> api/app -> api -> root
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from jailbreak_shield import JailbreakShield

router = APIRouter()

# Global shield instance (lazy loading)
_shield = None

def get_shield():
    global _shield
    if _shield is None:
        try:
            _shield = JailbreakShield(
                api_key=settings.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY"),
                layer2_enabled=settings.layer2_enabled
            )
        except Exception as e:
            print(f"Failed to initialize Shield: {e}")
            raise HTTPException(status_code=503, detail="Shield initialization failed")
    return _shield

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_prompt(request: AnalysisRequest, shield: JailbreakShield = Depends(get_shield)):
    """
    Analyze a prompt for jailbreak attempts using the multi-layer defense system.
    """
    try:
        # Override layer 2 if requested
        shield.layer2_enabled = request.layer2_enabled
        
        result = shield.defend(
            prompt=request.prompt,
            user_id=request.user_id,
            context=request.context
        )
        
        return AnalysisResponse(
            safe=result["safe"],
            risk_score=result["risk_score"],
            attack_detected=not result["safe"],
            attack_type=result.get("attack_type"),
            severity=result.get("severity"),
            explanation=result.get("explanation", "No explanation available"),
            recommendations=result.get("recommendations", []),
            latency_ms=result.get("latency_ms", 0.0),
            layer1_result=result.get("layer1_result", {}),
            layer2_result=result.get("layer2_result")
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Analysis engine error: {str(e)}")
