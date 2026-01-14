"""Vercel deployment helper for Streamlit"""
import streamlit as st
import os

# Configure Streamlit for Vercel
st.set_page_config(
    page_title="Jailbreak Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verify environment
if not os.getenv("ANTHROPIC_API_KEY"):
    st.warning("""
    ⚠️ ANTHROPIC_API_KEY not set!
    
    For Vercel deployment:
    1. Go to Vercel Dashboard
    2. Project Settings → Environment Variables
    3. Add: ANTHROPIC_API_KEY = sk-ant-...
    
    For local testing:
    - Create .env file with API key
    - Run: streamlit run demo/app.py
    """)
