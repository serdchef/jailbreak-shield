"""
FastAPI endpoint for Vercel deployment
Jailbreak Shield REST API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from jailbreak_shield import JailbreakShield

# Initialize FastAPI
app = FastAPI(
    title="Jailbreak Shield API",
    description="Prompt injection defense for Claude AI",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize shield
try:
    shield = JailbreakShield(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        layer2_enabled=os.getenv("LAYER2_ENABLED", "true").lower() == "true"
    )
except Exception as e:
    print(f"Warning: Shield initialization failed: {e}")
    shield = None


class PromptRequest(BaseModel):
    prompt: str
    layer2_enabled: bool = True


class PromptResponse(BaseModel):
    safe: bool
    risk_score: float
    attack_detected: bool
    attack_type: str | None
    explanation: str
    recommendations: list[str]
    layer1_flagged: bool
    layer2_flagged: bool | None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Jailbreak Shield API",
        "version": "0.1.0",
        "status": "operational",
        "endpoints": {
            "analyze": "/analyze",
            "health": "/health",
            "stats": "/stats"
        },
        "github": "https://github.com/serdchef/jailbreak-shield"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "shield_initialized": shield is not None,
        "layer2_available": shield is not None and shield.layer2 is not None if shield else False
    }


@app.post("/analyze", response_model=PromptResponse)
async def analyze_prompt(request: PromptRequest):
    """
    Analyze a prompt for jailbreak attempts
    
    Args:
        request: PromptRequest with prompt text
        
    Returns:
        PromptResponse with analysis results
    """
    if shield is None:
        raise HTTPException(
            status_code=503,
            detail="Shield not initialized. Check ANTHROPIC_API_KEY environment variable."
        )
    
    try:
        result = shield.defend(request.prompt)
        
        return PromptResponse(
            safe=result["safe"],
            risk_score=result["risk_score"],
            attack_detected=result["attack_detected"],
            attack_type=result["attack_type"],
            explanation=result["explanation"],
            recommendations=result["recommendations"],
            layer1_flagged=result["layer1_flagged"],
            layer2_flagged=result["layer2_flagged"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "total_analyzed": 0,  # TODO: Implement counter
        "blocked": 0,
        "allowed": 0,
        "layer1_triggers": 0,
        "layer2_triggers": 0
    }


# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
