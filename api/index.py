"""
api/index.py

Ultra-minimal API for Vercel Serverless (stays under 250MB)
Uses standard library + httpx only - no FastAPI, no Pydantic
"""
import json
import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import shield - but make sure it doesn't pull in heavy deps
from jailbreak_shield import JailbreakShield

# Global shield instance
_shield = None

def get_shield():
    global _shield
    if _shield is None:
        try:
            _shield = JailbreakShield(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                layer2_enabled=True,
                layer3_enabled=True,
                layer4_enabled=True
            )
        except Exception as e:
            print(f"Shield init failed: {e}")
            _shield = JailbreakShield(layer3_enabled=False)
    return _shield


class handler(BaseHTTPRequestHandler):
    """Vercel serverless handler using Python's built-in HTTP handler"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        if self.path == '/api/v1/health':
            response = {"status": "healthy", "engine": "ready"}
        elif self.path == '/api/v1/debug':
            api_key = os.getenv("ANTHROPIC_API_KEY")
            s = get_shield()
            response = {
                "api_key_present": bool(api_key),
                "api_key_length": len(api_key) if api_key else 0,
                "layer3_enabled": s.layer3_enabled,
            }
        elif self.path == '/api/v1/stats':
            s = get_shield()
            response = s.get_stats()
        else:
            response = {
                "status": "online",
                "engine": "Aegis 4-Layer",
                "version": "3.0.0"
            }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._send_error(400, "Invalid JSON")
            return
        
        if self.path == '/api/v1/analyze':
            prompt = data.get('prompt', '')
            user_id = data.get('user_id', 'web_default')
            
            if not prompt:
                self._send_error(400, "prompt is required")
                return
            
            s = get_shield()
            try:
                result = s.defend(prompt, user_id=user_id)
                self._send_json(200, result)
            except Exception as e:
                self._send_error(500, str(e))
        else:
            self._send_error(404, "Not found")
    
    def _send_json(self, status, data):
        self.send_response(status)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error(self, status, message):
        self.send_response(status)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())
    
    def _send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass
