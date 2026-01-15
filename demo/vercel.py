"""
Vercel için ASGI wrapper - Streamlit deployment
"""
import os
import sys
import streamlit as st
from pathlib import Path

# Streamlit config für Vercel
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_PORT"] = "3000"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "true"

# Import the main app
sys.path.insert(0, str(Path(__file__).parent))

from app import *
