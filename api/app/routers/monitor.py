from fastapi import APIRouter, Depends
from ..models import StatsResponse
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from jailbreak_shield import JailbreakShield

router = APIRouter()

# Singleton for this router if used independently
_shield = None

def get_shield_instance():
    global _shield
    if _shield is None:
        _shield = JailbreakShield()
    return _shield

@router.get("/stats", response_model=StatsResponse)
async def get_system_stats():
    """
    Get real-time system statistics and health metrics.
    """
    shield_instance = get_shield_instance()
    stats = shield_instance.get_stats()
    
    # Map shield stats to StatsResponse if necessary, or return directly
    # For now, we return a mock-like structure populated with real data where possible
    # or just return the dict if the model allows it.
    
    return StatsResponse(
        total_requests=stats.get("metrics", {}).get("total_requests", 0),
        blocked_requests=stats.get("metrics", {}).get("blocked_requests", 0),
        avg_latency=stats.get("metrics", {}).get("avg_latency", 0.0),
        active_layers=[k for k,v in stats.get("layers", {}).items() if v["status"] == "active"]
    )
