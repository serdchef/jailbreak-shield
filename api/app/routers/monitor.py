from fastapi import APIRouter
from ..models import StatsResponse

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def get_system_stats():
    """
    Get real-time system statistics and health metrics.
    """
    # TODO: Connect to actual metrics collector
    return StatsResponse(
        total_requests=1245,
        blocked_requests=138,
        avg_latency=45.2,
        active_layers=["Static Analysis (Layer 1)", "Semantic Analysis (Layer 2)"]
    )
