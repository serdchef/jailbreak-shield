# Deployment Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Docker](#docker)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Setup](#production-setup)
5. [Monitoring & Logging](#monitoring--logging)
6. [Security Best Practices](#security-best-practices)

---

## Local Development

### Prerequisites
- Python 3.8+
- pip
- ANTHROPIC_API_KEY

### Setup

```bash
# Clone repository
git clone https://github.com/serdchef/jailbreak-shield
cd jailbreak-shield

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy .env template
cp .env.example .env

# Edit .env with your API key
# ANTHROPIC_API_KEY=sk-...
```

### Testing

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_layer1.py -v

# Run with coverage
pytest --cov=jailbreak_shield tests/
```

### Local Demo

```bash
# Install demo dependencies
pip install -r demo/requirements.txt

# Run Streamlit app
streamlit run demo/app.py

# Open http://localhost:8501
```

---

## Docker

### Build Image

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "-c", "from jailbreak_shield import JailbreakShield; print('Ready')"]
```

### Build and Run

```bash
# Build image
docker build -t jailbreak-shield:0.1.0 .

# Run container
docker run \
  -e ANTHROPIC_API_KEY=sk-... \
  jailbreak-shield:0.1.0

# Run demo
docker run \
  -p 8501:8501 \
  -e ANTHROPIC_API_KEY=sk-... \
  jailbreak-shield:0.1.0 \
  streamlit run demo/app.py --server.port 8501
```

### Docker Compose

```yaml
version: '3.8'

services:
  shield:
    build: .
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
      LAYER2_ENABLED: "true"
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
```

Run with:
```bash
docker-compose up
```

---

## Cloud Deployment

### Streamlit Cloud (Free Demo)

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. New app → Select repository
4. Set secrets in Streamlit dashboard:
   ```
   ANTHROPIC_API_KEY = sk-...
   ```
5. Deploy

### AWS Lambda (Serverless)

```python
# lambda_handler.py
from jailbreak_shield import JailbreakShield
import json

shield = JailbreakShield()

def lambda_handler(event, context):
    prompt = json.loads(event['body'])['prompt']
    result = shield.defend(prompt)
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

Deploy with:
```bash
serverless deploy
```

### Google Cloud Run

```bash
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT main:app
```

Deploy:
```bash
gcloud run deploy shield \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars ANTHROPIC_API_KEY=sk-...
```

### DigitalOcean App Platform

1. Connect GitHub repo
2. Create app
3. Set environment variables
4. Deploy

---

## Production Setup

### API Wrapper

```python
# api.py
from fastapi import FastAPI, HTTPException
from jailbreak_shield import JailbreakShield
import os

app = FastAPI()
shield = JailbreakShield()

@app.post("/defend")
async def defend(request: dict):
    try:
        prompt = request.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Missing prompt")
        
        result = shield.defend(prompt)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}
```

Run with:
```bash
pip install fastapi uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Database Logging

```python
# With SQLite
import sqlite3
from datetime import datetime

def log_defense_result(prompt, result):
    conn = sqlite3.connect('jailbreak_shield.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO defense_events 
        (prompt, safe, risk_score, attack_type, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        prompt[:1000],  # Store first 1000 chars
        result['safe'],
        result['risk_score'],
        result['attack_type'],
        datetime.now()
    ))
    
    conn.commit()
    conn.close()

# Create table
def init_db():
    conn = sqlite3.connect('jailbreak_shield.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS defense_events (
            id INTEGER PRIMARY KEY,
            prompt TEXT,
            safe BOOLEAN,
            risk_score FLOAT,
            attack_type TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()
```

### Async Processing

```python
# For high-volume scenarios
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=10)

async def defend_async(prompt):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        executor,
        shield.defend,
        prompt
    )
    return result

# Batch processing
async def batch_defend(prompts):
    tasks = [defend_async(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

---

## Monitoring & Logging

### Application Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('shield.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def defend_with_logging(prompt):
    logger.info(f"Analyzing prompt: {prompt[:50]}...")
    result = shield.defend(prompt)
    logger.info(f"Result: {result['attack_detected']}")
    return result
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, start_http_server

# Metrics
attacks_detected = Counter('attacks_detected', 'Total attacks detected')
false_positives = Counter('false_positives', 'False positive detections')
defense_latency = Histogram('defense_latency_ms', 'Defense latency in ms')

@defense_latency.time()
def defend_with_metrics(prompt):
    result = shield.defend(prompt)
    if result['attack_detected']:
        attacks_detected.inc()
    return result

# Start metrics server
start_http_server(8000)
```

### Alerting

Set up alerts for:
- High attack detection rate
- API errors
- High latency
- Cost overruns

---

## Security Best Practices

### API Key Management

```bash
# ✅ DO: Use environment variables
export ANTHROPIC_API_KEY=sk-...

# ✅ DO: Use secrets management
# AWS Secrets Manager
# Google Secret Manager
# HashiCorp Vault

# ✅ DO: Rotate regularly
# Every 90 days minimum

# ❌ DON'T: Hardcode keys
# ❌ DON'T: Commit to git
# ❌ DON'T: Log API keys
```

### Input Validation

```python
def validate_prompt(prompt):
    if not isinstance(prompt, str):
        raise ValueError("Prompt must be string")
    if len(prompt) > 100000:
        raise ValueError("Prompt too long")
    if not prompt.strip():
        raise ValueError("Prompt empty")
    return True
```

### Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/defend")
@limiter.limit("100/minute")
async def defend(request):
    # Your code
```

### HTTPS/TLS

```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Use in FastAPI
uvicorn api:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### Access Control

```python
from fastapi.security import HTTPBearer, HTTPAuthCredential

security = HTTPBearer()

@app.post("/defend")
async def defend(request, credentials: HTTPAuthCredential = None):
    if not verify_token(credentials.credentials):
        raise HTTPException(status_code=401)
    # Your code
```

---

## Cost Optimization

### Layer 1 Only Strategy

```python
# For high-volume, use Layer 1 only
shield = JailbreakShield(layer2_enabled=False)
# 10ms, $0 per request
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def defend_cached(prompt):
    return shield.defend(prompt)
```

### Batch Processing

```python
# Process multiple prompts in single API call
prompts = ["prompt1", "prompt2", ...]
results = [shield.defend(p) for p in prompts]
```

---

## Maintenance

### Regular Tasks

- [ ] Update dependencies monthly
- [ ] Review error logs weekly
- [ ] Check API costs monthly
- [ ] Rotate API keys quarterly
- [ ] Test disaster recovery biannually

### Updates

```bash
pip install --upgrade jailbreak-shield
pip install -r requirements.txt --upgrade
```

### Backup

```bash
# Back up logs and database
cp shield.log shields.log.$(date +%Y%m%d)
cp jailbreak_shield.db jailbreak_shield.db.$(date +%Y%m%d)
```

---

## Troubleshooting

### Issue: "ANTHROPIC_API_KEY not set"

```bash
# Set environment variable
export ANTHROPIC_API_KEY=sk-...

# Or create .env file
echo "ANTHROPIC_API_KEY=sk-..." > .env
```

### Issue: High latency

```python
# Use Layer 1 only
shield = JailbreakShield(layer2_enabled=False)

# Increase concurrency
# Implement caching
# Use batch processing
```

### Issue: High costs

```python
# Reduce Layer 2 usage
shield = JailbreakShield(layer2_threshold=0.8)

# Cache results
# Use Layer 1 only for most requests
# Implement rate limiting
```

---

For additional help, see [GitHub Issues](https://github.com/serdchef/jailbreak-shield/issues)
