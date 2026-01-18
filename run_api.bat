@echo off
echo Starting Jailbreak Shield "Aegis" API...
cd %~dp0
uvicorn api.app.main:app --reload --port 8000
