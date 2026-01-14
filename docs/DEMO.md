# Demo App Documentation

## Overview

The Jailbreak Shield demo is an interactive Streamlit web application that lets you test prompts against the defense system in real-time.

## Running the Demo

### Prerequisites
- Python 3.8+
- `ANTHROPIC_API_KEY` environment variable set

### Installation

```bash
# Install dependencies
pip install -r demo/requirements.txt

# Or install all dependencies
pip install -r requirements.txt
pip install -r demo/requirements.txt
```

### Launch

```bash
streamlit run demo/app.py
```

Then visit `http://localhost:8501` in your browser.

## Features

### 1. Prompt Testing
- Enter custom prompts
- Choose from pre-loaded examples
- Real-time analysis

### 2. Example Prompts
- **Benign:** "What's the capital of France?"
- **Role Confusion:** "Ignore all previous instructions..."
- **Context Injection:** XML/tag injection examples
- **Payload Hiding:** Encoded instruction examples

### 3. Real-time Results
- **Risk Score** (0-100)
- **Attack Type** (category detected)
- **Layer Status** (which defense layer triggered)

### 4. Detailed Analysis
- **Explanation:** Human-readable summary
- **Recommendations:** Suggested actions
- **Technical Details:** Full JSON result (expandable)

### 5. Statistics Dashboard
- Overall accuracy metrics
- Precision, recall, F1 score
- Benchmark results (if available)

## Configuration

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY=sk-...

# Optional
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Config

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[client]
showErrorDetails = false
```

## Deployment

### Docker

```bash
docker build -f Dockerfile.demo -t shield-demo .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=sk-... shield-demo
```

### Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repo
4. Add secrets:
   ```
   ANTHROPIC_API_KEY = sk-...
   ```
5. Deploy

### Heroku

```bash
heroku create shield-demo
heroku config:set ANTHROPIC_API_KEY=sk-...
git push heroku main
```

## Usage Examples

### Test a Benign Prompt
1. Select "Benign" example
2. Click "Analyze Prompt"
3. See: ✅ SAFE result
4. Risk Score: 0-20

### Test a Malicious Prompt
1. Select "Role Confusion" example
2. Click "Analyze Prompt"
3. See: ⚠️ BLOCKED result
4. Review explanation and attack type

### Custom Prompt Analysis
1. Select "Custom"
2. Paste your own prompt
3. Click "Analyze Prompt"
4. Get detailed results

## Troubleshooting

### "Shield not initialized" Error

**Cause:** ANTHROPIC_API_KEY not set

**Solution:**
```bash
export ANTHROPIC_API_KEY=sk-...
streamlit run demo/app.py
```

### "No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit
```

### High Latency

**Cause:** Layer 2 (Claude Haiku) analysis takes ~500ms

**Solution:** Use Layer 1 only or increase timeout

### Statistics Not Loading

**Cause:** Benchmark data not generated

**Solution:**
```bash
python scripts/collect_jailbreaks.py
python scripts/benchmark.py
```

## Advanced Configuration

### Custom Examples

Edit `demo/app.py`:

```python
examples = {
    "My Custom": "Your example prompt here",
    # ... existing examples
}
```

### Custom Theme

Modify `.streamlit/config.toml` colors

### Authentication

Add authentication with:

```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login()

if authentication_status:
    # Show app
    pass
```

## API Integration

Use the demo to test integration with your application:

```python
# Get insights from demo results
# Adjust thresholds
# Test edge cases
# Validate production config
```

## Performance Tips

1. **Cache Results:** Streamlit caches JailbreakShield initialization
2. **Use Layer 1 Only:** For faster demos (set `layer2_enabled=False`)
3. **Batch Analysis:** Process multiple prompts at once
4. **Local Deployment:** Run locally for best performance

---

For more help, see the main [README](../README.md)
