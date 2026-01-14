#!/bin/bash
# 🚀 Jailbreak Shield - Quick Launch Commands

# ============================================================================
# STEP 1: Prepare Local Repository (Already Done ✅)
# ============================================================================
# These have already been executed:
# git init
# git config user.name "Your Name"
# git config user.email "your@email.com"
# git add .
# git commit -m "🛡️ Jailbreak Shield v0.1.0"

# ============================================================================
# STEP 2: Push to GitHub (DO THIS NEXT!)
# ============================================================================

# First, create the GitHub repo at: https://github.com/new
# Name: jailbreak-shield
# Description: "Open-source prompt injection defense for Claude AI"
# Public: Yes
# Then run these commands:

cd c:\Users\x\Desktop\shield
git remote add origin https://github.com/YOUR_USERNAME/jailbreak-shield.git
git branch -M main
git push -u origin main

# ============================================================================
# STEP 3: Deploy to Vercel
# ============================================================================

# Option A: Via Vercel Dashboard
# 1. Go to https://vercel.com/new
# 2. Click "Import Git Repository"
# 3. Select jailbreak-shield
# 4. Add environment variables (see below)
# 5. Deploy

# Option B: Via Vercel CLI
npm install -g vercel
cd c:\Users\x\Desktop\shield
vercel --prod

# Environment Variables to Add:
# ANTHROPIC_API_KEY=sk-ant-v0.1... (your actual key)
# LAYER2_ENABLED=true
# LAYER2_THRESHOLD=0.5
# LOG_LEVEL=INFO

# ============================================================================
# STEP 4: Verify Deployment
# ============================================================================

# Check that your live demo is at:
# https://jailbreak-shield.vercel.app
# (or your custom Vercel URL)

# ============================================================================
# STEP 5: Test Everything Locally (Optional but Recommended)
# ============================================================================

# Install package in development mode
cd c:\Users\x\Desktop\shield
pip install -e .

# Run tests
pytest tests/ -v

# Run benchmark
python scripts/benchmark_l1_only.py

# Run demo locally
streamlit run demo/app.py
# Visit: http://localhost:8501

# ============================================================================
# STEP 6: Update README with Live Demo Link
# ============================================================================

# Edit README.md, update this section:
# ## 🎮 Try the Demo
# [![Live Demo](https://img.shields.io/badge/Demo-Live-brightgreen)](https://jailbreak-shield.vercel.app)
# Or visit: https://jailbreak-shield.vercel.app

# ============================================================================
# STEP 7: Publish Blog Posts
# ============================================================================

# Copy content from BLOG_POST_DRAFT.md and post on:

# Medium: https://medium.com/new-story
# Dev.to: https://dev.to/new
# Hashnode: https://hashnode.com/create

# In each, include:
# - GitHub link: https://github.com/YOUR_USERNAME/jailbreak-shield
# - Live demo link: https://jailbreak-shield.vercel.app
# - Key metrics and benchmarks

# ============================================================================
# STEP 8: Launch on Social Media
# ============================================================================

# Twitter: Post thread from SOCIAL_MEDIA_CONTENT.md
# - Thread with 7-8 tweets explaining the project
# - Include links to GitHub and demo
# - Hashtags: #security #ai #python #claude #opensource

# LinkedIn: Post professional version
# - Share article + key metrics
# - Mention Anthropic and community focus
# - Link to blog post and GitHub

# Reddit: Post to relevant communities
# Communities:
# - r/MachineLearning
# - r/ChatGPT
# - r/Python
# - r/opensource
# - r/cybersecurity

# Hacker News: Submit via https://news.ycombinator.com/submit
# Title: "Jailbreak Shield – Open-source prompt injection defense for Claude"
# URL: https://github.com/YOUR_USERNAME/jailbreak-shield

# ============================================================================
# STEP 9: Email Outreach
# ============================================================================

# Send emails to:

# Anthropic Security Team:
# Subject: Jailbreak Shield - Open-Source Prompt Injection Defense
# Content: See SOCIAL_MEDIA_CONTENT.md > Email Template

# Friends/Colleagues:
# Ask them to:
# - Star the repo
# - Try the demo
# - Share in their networks

# ============================================================================
# STEP 10: Monitor & Respond
# ============================================================================

# Watch for engagement on:
# - GitHub: Answer issues, review PRs
# - Twitter: Respond to mentions/replies
# - Reddit: Engage in discussions
# - Email: Reply to inquiries

# Track metrics:
# - GitHub stars
# - Demo usage
# - Social media engagement
# - Community contributions

# ============================================================================
# STEP 11: Submit Builder Club Application (Day 3-5)
# ============================================================================

# Go to: https://builders.anthropic.com
# Complete form with:
# - Project title: Jailbreak Shield
# - GitHub: https://github.com/YOUR_USERNAME/jailbreak-shield
# - Demo: https://jailbreak-shield.vercel.app
# - Blog: https://[blog-platform]/jailbreak-shield
# - Metrics: GitHub stars, demo users, community engagement
# - Vision: Community-driven AI security

# ============================================================================
# OPTIONAL: Setup GitHub Pages (Documentation Site)
# ============================================================================

# Enable GitHub Pages:
# 1. Go to repo Settings > Pages
# 2. Set source to: main branch /docs folder
# 3. Your docs will be at: https://YOUR_USERNAME.github.io/jailbreak-shield

# Or use MkDocs for better documentation:
# pip install mkdocs mkdocs-material
# mkdocs build
# mkdocs deploy

# ============================================================================
# OPTIONAL: Setup GitHub Actions (CI/CD)
# ============================================================================

# Create .github/workflows/tests.yml:
# - Run tests on every push
# - Check code quality
# - Validate documentation

# Create .github/workflows/deploy.yml:
# - Auto-deploy to Vercel on push to main

# ============================================================================
# USEFUL COMMANDS FOR ONGOING MAINTENANCE
# ============================================================================

# Check status
git status

# View commit history
git log --oneline

# Update dependencies
pip install --upgrade -r requirements.txt

# Check for security issues
pip install safety
safety check

# View test coverage
pytest --cov=jailbreak_shield

# Format code
pip install black
black jailbreak_shield/ tests/ scripts/

# Lint code
pip install pylint
pylint jailbreak_shield/

# Type checking
pip install mypy
mypy jailbreak_shield/

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

# Copy and paste this daily to track progress:

echo "=== Jailbreak Shield Launch Progress ===" 
echo "GitHub Stars: $(curl -s https://api.github.com/repos/YOUR_USERNAME/jailbreak-shield | grep stargazers_count | awk '{print $2}')"
echo "Demo Visitors: [Check Vercel Analytics]"
echo "GitHub Issues: [Check GitHub]"
echo "Community PRs: [Check GitHub]"

# ============================================================================
# COMMON ISSUES & SOLUTIONS
# ============================================================================

# Issue: "fatal: remote origin already exists"
# Solution: git remote remove origin
#         git remote add origin https://...

# Issue: "ModuleNotFoundError: No module named 'jailbreak_shield'"
# Solution: pip install -e .

# Issue: "ANTHROPIC_API_KEY not found"
# Solution: Set environment variable or use .env file
#         export ANTHROPIC_API_KEY=your_key_here

# Issue: "Vercel deployment fails"
# Solution: Check vercel.json syntax, env vars, Python version
#         vercel logs

# Issue: "Streamlit demo not loading"
# Solution: Check port 8501 is free
#         streamlit run demo/app.py --server.port 8502

# ============================================================================
# FILES TO REMEMBER
# ============================================================================

# READ THESE FIRST:
# 1. README.md - Project overview
# 2. QUICKSTART.md - 5-minute setup
# 3. PROJECT_STATUS.md - Current status (you are here!)
# 4. LAUNCH_CHECKLIST.md - Step-by-step plan

# FOR LAUNCH:
# 1. BLOG_POST_DRAFT.md - Use for blog posts
# 2. SOCIAL_MEDIA_CONTENT.md - Use for social media
# 3. VERCEL_DEPLOYMENT.md - Use for Vercel setup
# 4. LAUNCH_CHECKLIST.md - Use to track progress

# FOR DEVELOPMENT:
# 1. docs/ARCHITECTURE.md - Technical design
# 2. docs/API.md - API reference
# 3. docs/DEPLOYMENT.md - Production setup

# ============================================================================
# 🎉 YOU'RE READY TO LAUNCH!
# ============================================================================

# Next step: Create GitHub repo at https://github.com/new
# Then run the commands in STEP 2 above

# Questions? Check docs/ folder or email a.serdcarl@gmail.com
