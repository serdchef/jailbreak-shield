#!/usr/bin/env bash
# Vercel deployment script
set -e

echo "📦 Installing dependencies..."
pip install -r demo/requirements.txt

echo "✅ Deployment ready!"
echo "🚀 Run locally: streamlit run demo/app.py"
echo "🌐 Deploy to Vercel: vercel --prod"
