"""
api/index.py

FastAPI endpoint for Vercel deployment (World-Class 4-Layer Edition)
Jailbreak Shield REST API
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import time
from typing import Dict, Optional, List
from pathlib import Path

# Add project root to path so we can import jailbreak_shield
sys.path.insert(0, str(Path(__file__).parent.parent))

from jailbreak_shield import JailbreakShield

# Initialize FastAPI
app = FastAPI(
    title="Jailbreak Shield Aegis API",
    description="Enterprise-grade prompt injection defense (4-Layer Grid)",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize shield globally for persistence in serverless environments
shield = None

def get_shield():
    global shield
    if shield is None:
        try:
            shield = JailbreakShield(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                layer2_enabled=True,
                layer3_enabled=True,
                layer4_enabled=True
            )
        except Exception as e:
            print(f"⚠️ Shield initialization failed: {e}")
            # Fallback to a basic instance if possible
            shield = JailbreakShield(layer3_enabled=False)
    return shield

class AnalysisRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = "web_default"

@app.get("/api/v1")
async def root():
    return {
        "status": "online",
        "engine": "Aegis 4-Layer",
        "version": "3.0.0"
    }

@app.get("/api/v1/health")
async def health():
    return {"status": "healthy", "engine": "ready"}

@app.post("/api/v1/analyze")
async def analyze(request: AnalysisRequest):
    s = get_shield()
    try:
        result = s.defend(request.prompt, user_id=request.user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/stats")
async def stats():
    s = get_shield()
    return s.get_stats()

# For Vercel, the app must be at the top level
# but for internal routing, we use /api/*
