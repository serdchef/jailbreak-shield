from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import analyze, monitor
from .config import settings

app = FastAPI(
    title="Jailbreak Shield Aegis API",
    description="World-class enterprise defense system for LLMs",
    version="2.0.0",
    redoc_url=None
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(monitor.router, prefix="/api/v1", tags=["Monitoring"])

@app.get("/")
async def root():
    return {
        "system": "Jailbreak Shield Aegis",
        "status": "operational",
        "version": "2.0.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
