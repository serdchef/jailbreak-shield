# 🚀 Vercel Deployment Guide

This guide walks you through deploying Jailbreak Shield's Streamlit demo to Vercel.

## Prerequisites

1. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account** - Your project repository
3. **Anthropic API Key** - For Layer 2 semantic analysis
4. **Git** - For version control

## Step 1: Push to GitHub

First, ensure your repo is on GitHub:

```bash
# Initialize if not already done
git init
git add .
git commit -m "Initial commit: Jailbreak Shield"

# Create new repo on github.com/new
# Then:
git remote add origin https://github.com/YOUR_USERNAME/jailbreak-shield.git
git branch -M main
git push -u origin main
```

## Step 2: Connect to Vercel

### Option A: Using Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Git Repository"
3. Select your `jailbreak-shield` repository
4. Vercel will auto-detect the configuration

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from project directory
cd jailbreak-shield
vercel
```

## Step 3: Configure Environment Variables

In Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add the following variables:

```
ANTHROPIC_API_KEY=sk-ant-v0.1... (your actual key)
LAYER2_ENABLED=true
LAYER2_THRESHOLD=0.5
LOG_LEVEL=INFO
```

**Important:** Never commit your API key! Use Vercel's environment variable system.

## Step 4: Configure Build Settings

Vercel should auto-detect, but verify:

- **Framework**: Python (or "Other")
- **Build Command**: `pip install -r demo/requirements.txt`
- **Output Directory**: (leave empty for Streamlit)
- **Install Command**: `pip install -r demo/requirements.txt`

## Step 5: Deploy

Option A (Dashboard):
```
Click "Deploy" button on Vercel dashboard
```

Option B (CLI):
```bash
vercel --prod
```

## Step 6: Access Your Demo

Your Streamlit app will be live at:
```
https://jailbreak-shield.vercel.app
```

(Replace with your actual Vercel project name)

## Troubleshooting

### "ModuleNotFoundError: No module named 'jailbreak_shield'"

Solution: Ensure your `vercel.json` has correct build command:
```json
{
  "buildCommand": "pip install -r demo/requirements.txt && pip install -e ..",
  ...
}
```

### "ANTHROPIC_API_KEY not found"

Solution: 
1. Check Vercel environment variables are set
2. Redeploy after adding variables
3. Use Vercel CLI: `vercel env pull` to test locally

### Streamlit Port Issues

Streamlit requires port 3000 on Vercel. The `vercel.json` should have:
```json
{
  "routes": [
    {"src": "/(.*)", "dest": "demo/app.py"}
  ]
}
```

### Slow Response Times

Vercel Serverless functions have cold start times. For production:
1. Consider AWS Lambda with Vercel integration
2. Use Vercel Edge Functions (faster)
3. Keep dependencies minimal

## Keeping Deployment Updated

To update your live demo with code changes:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Vercel will auto-redeploy on push to main
```

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes | N/A |
| `LAYER2_ENABLED` | Enable semantic analysis | No | true |
| `LAYER2_THRESHOLD` | Risk threshold (0-1) | No | 0.5 |
| `LOG_LEVEL` | Logging level | No | INFO |

## Custom Domain

To use a custom domain:

1. In Vercel dashboard → Settings → Domains
2. Add your custom domain
3. Update DNS records according to Vercel's instructions

Example: `shield.yourdomain.com`

## Monitoring & Logs

View deployment logs in Vercel dashboard:
1. Select your project
2. Go to "Deployments" tab
3. Click any deployment to view logs
4. Check both "Build" and "Runtime" logs

## Cost Considerations

**Vercel Pricing (as of 2024):**
- Hobby tier: Free (limited)
- Pro tier: $20/month
- Cost is per deployment + API calls

**Optimize Costs:**
1. Use Vercel's automatic scaling
2. Keep API calls minimal (Layer 1 only for most requests)
3. Use Vercel analytics to monitor usage
4. Consider setting up alerts for high costs

## Performance Tips

### 1. Lazy Load Dependencies
Only import Anthropic when Layer 2 is needed:
```python
if layer2_enabled:
    from anthropic import Anthropic
```

### 2. Cache Results
Consider caching Layer 2 analysis for identical prompts:
```python
@lru_cache(maxsize=1000)
def analyze_semantic(prompt):
    ...
```

### 3. Use Vercel Edge Functions
For ultra-low latency (experimental):
```json
{
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1",
      "middlewares": ["middleware.js"]
    }
  ]
}
```

## Security Best Practices

1. **Never commit API keys** - Use Vercel env vars only
2. **Enable CORS carefully** - Restrict to your domain
3. **Add rate limiting** - Prevent abuse
4. **Monitor costs** - Set spending alerts
5. **Rotate API keys** - Regularly update credentials

Example CORS in Streamlit:
```python
import streamlit as st

st.set_page_config(
    page_title="Jailbreak Shield",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Add security headers
headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block"
}
```

## Advanced: Using Vercel with GitHub Actions

For CI/CD pipeline:

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: vercel/action@v4
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

## Support & Help

- **Vercel Docs**: https://vercel.com/docs
- **Streamlit Docs**: https://docs.streamlit.io
- **GitHub Issues**: [jailbreak-shield issues]
- **Email**: a.serdcarl@gmail.com

---

**Next Steps:**
1. ✅ Deploy to Vercel
2. ✅ Get live demo URL
3. ✅ Add to README
4. ✅ Share with community
