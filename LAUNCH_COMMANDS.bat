@echo off
REM 🚀 Jailbreak Shield - Quick Launch Commands for Windows
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║        🛡️  JAILBREAK SHIELD - LAUNCH COMMANDS FOR WINDOWS             ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM ============================================================================
REM STEP 1: Verify Local Repository
REM ============================================================================

echo STEP 1: Verifying local repository...
cd c:\Users\x\Desktop\shield
git log --oneline -3
echo ✅ Repository initialized with commits

REM ============================================================================
REM STEP 2: Push to GitHub
REM ============================================================================

echo.
echo STEP 2: Push to GitHub
echo Before proceeding:
echo   1. Go to: https://github.com/new
echo   2. Create new repo named: jailbreak-shield
echo   3. Description: "Open-source prompt injection defense for Claude AI"
echo   4. Public: Yes
echo   5. Then run these commands:
echo.
echo   git remote add origin https://github.com/YOUR_USERNAME/jailbreak-shield.git
echo   git branch -M main
echo   git push -u origin main
echo.
pause

REM Uncomment and fill in YOUR_USERNAME to auto-run:
REM git remote add origin https://github.com/YOUR_USERNAME/jailbreak-shield.git
REM git branch -M main
REM git push -u origin main

REM ============================================================================
REM STEP 3: Setup for Vercel Deployment
REM ============================================================================

echo.
echo STEP 3: Vercel Deployment Setup
echo.
echo Option A - Via Web:
echo   1. Go to: https://vercel.com/new
echo   2. Click "Import Git Repository"
echo   3. Select: jailbreak-shield
echo   4. Add Environment Variables:
echo      - ANTHROPIC_API_KEY=sk-ant-... (your actual key)
echo      - LAYER2_ENABLED=true
echo      - LAYER2_THRESHOLD=0.5
echo      - LOG_LEVEL=INFO
echo   5. Deploy
echo.
echo Option B - Via Vercel CLI (if installed):
echo   vercel --prod
echo.

REM ============================================================================
REM STEP 4: Run Tests Locally
REM ============================================================================

echo.
echo STEP 4: Run Tests Locally
echo.
cd c:\Users\x\Desktop\shield
echo Testing Layer 1 Benchmark...
python scripts/benchmark_l1_only.py
echo ✅ Benchmark complete
echo.
pause

REM ============================================================================
REM STEP 5: Launch Streamlit Demo Locally
REM ============================================================================

echo.
echo STEP 5: Test Streamlit Demo Locally
echo.
echo Running: streamlit run demo/app.py
echo Open browser at: http://localhost:8501
echo.
REM Uncomment to run:
REM streamlit run demo/app.py
echo.
pause

REM ============================================================================
REM STEP 6: Update README
REM ============================================================================

echo.
echo STEP 6: Update README.md
echo.
echo Add your live demo URL to README.md:
echo   1. After deploying to Vercel, get your URL
echo   2. Replace VERCEL_URL with actual URL
echo   3. Update section: "## 🎮 Try the Demo"
echo.

REM ============================================================================
REM STEP 7: Publish Blog Posts
REM ============================================================================

echo.
echo STEP 7: Publish Blog Posts
echo.
echo Copy content from BLOG_POST_DRAFT.md and post on:
echo   - Medium: https://medium.com/new-story
echo   - Dev.to: https://dev.to/new
echo   - Hashnode: https://hashnode.com/create
echo.
echo Include in each post:
echo   - GitHub: https://github.com/YOUR_USERNAME/jailbreak-shield
echo   - Live Demo: https://jailbreak-shield.vercel.app
echo   - Key metrics from benchmarks
echo.

REM ============================================================================
REM STEP 8: Launch on Social Media
REM ============================================================================

echo.
echo STEP 8: Launch on Social Media
echo.
echo Twitter Thread:
echo   - Use content from SOCIAL_MEDIA_CONTENT.md
echo   - Post 7-8 tweets in thread
echo   - Include links and metrics
echo.
echo LinkedIn Post:
echo   - Professional version with company angle
echo   - Share blog post link
echo   - Target: Security professionals
echo.
echo Reddit Posts:
echo   - r/MachineLearning
echo   - r/ChatGPT
echo   - r/Python
echo   - r/opensource
echo.
echo Hacker News:
echo   - Submit at: https://news.ycombinator.com/submit
echo   - Title: "Jailbreak Shield – Open-source prompt injection defense"
echo   - URL: GitHub repo link
echo.

REM ============================================================================
REM STEP 9: Monitor Engagement
REM ============================================================================

echo.
echo STEP 9: Monitor and Track Progress
echo.
echo Check these daily:
echo   - GitHub: Star count, issues, PRs
echo   - Vercel: Demo usage, analytics
echo   - Twitter: Mentions, likes, retweets
echo   - LinkedIn: Views, comments
echo   - Reddit: Upvotes, comments
echo.
echo Key Files to Monitor:
echo   - PROJECT_STATUS.md - Update metrics
echo   - LAUNCH_CHECKLIST.md - Track progress
echo.

REM ============================================================================
REM STEP 10: Builder Club Application
REM ============================================================================

echo.
echo STEP 10: Submit Builder Club Application (Day 3-5)
echo.
echo Go to: https://builders.anthropic.com
echo.
echo In application, include:
echo   - Project title: Jailbreak Shield
echo   - GitHub: https://github.com/YOUR_USERNAME/jailbreak-shield
echo   - Demo: https://jailbreak-shield.vercel.app
echo   - Blog: [Your blog post URL]
echo   - Current metrics (stars, demo users, etc.)
echo   - Vision statement
echo.

REM ============================================================================
REM USEFUL COMMANDS
REM ============================================================================

echo.
echo USEFUL COMMANDS FOR DEVELOPMENT
echo.
echo View git history:
echo   git log --oneline
echo.
echo Check status:
echo   git status
echo.
echo Install package for development:
echo   pip install -e .
echo.
echo Run all tests:
echo   pytest tests/ -v
echo.
echo Format code:
echo   pip install black
echo   black jailbreak_shield/ tests/ scripts/
echo.
echo Lint code:
echo   pip install pylint
echo   pylint jailbreak_shield/
echo.

REM ============================================================================
REM FILES TO REMEMBER
REM ============================================================================

echo.
echo 📁 IMPORTANT FILES
echo.
echo READ FIRST:
echo   - README.md - Project overview
echo   - QUICKSTART.md - 5-minute setup
echo   - PROJECT_STATUS.md - Current status
echo   - LAUNCH_CHECKLIST.md - Step-by-step plan
echo.
echo FOR LAUNCHING:
echo   - BLOG_POST_DRAFT.md - Copy for blog
echo   - SOCIAL_MEDIA_CONTENT.md - Copy for social
echo   - VERCEL_DEPLOYMENT.md - Vercel setup
echo   - LAUNCH_CHECKLIST.md - Track progress
echo.
echo FOR DEVELOPMENT:
echo   - docs/ARCHITECTURE.md - Technical design
echo   - docs/API.md - API reference
echo   - docs/DEPLOYMENT.md - Production setup
echo.

REM ============================================================================
REM FINAL STATUS
REM ============================================================================

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                     ✅ YOU'RE READY TO LAUNCH!                         ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo Next Step: Create GitHub repo at https://github.com/new
echo Then push code using Step 2 commands above
echo.
echo Questions? Check docs/ folder or email: a.serdcarl@gmail.com
echo.

pause
