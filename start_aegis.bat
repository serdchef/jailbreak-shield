@echo off
echo ===================================================
echo    JAILBREAK SHIELD AEGIS // INITIALIZING...
echo ===================================================

echo [1/2] Starting Neural Core (FastAPI Backend)...
start "Aegis Backend" cmd /k "call .env && uvicorn api.app.main:app --reload --port 8000"

echo [2/2] Launching Command Center (Next.js Frontend)...
cd web
start "Aegis Command Center" cmd /k "npm run dev"

echo.
echo SYSTEM ONLINE.
echo Access Command Center at: http://localhost:3001
echo.
pause
