# Architecture Guide

## System Overview

Jailbreak Shield implements a two-layer defense system optimized for speed and cost-effectiveness.

### Layer 1: Static Pattern Analysis

**Characteristics:**
- Execution time: ~10ms
- Cost: $0
- Coverage: 80% of known attacks

**Detection Methods:**
1. **Regex Pattern Matching** - Known attack signatures
2. **Keyword Detection** - Suspicious phrases
3. **Structural Analysis** - XML injection, excessive newlines, unicode abuse
4. **Heuristic Scoring** - Length, repetition, vocabulary analysis

### Layer 2: Semantic Analysis

**Characteristics:**
- Execution time: ~500ms
- Cost: ~$0.001 per call
- Coverage: 15% additional attacks Layer 1 misses
- Used only when Layer 1 flags something suspicious

**Detection Methods:**
1. **Intent Analysis** - Claude Haiku contextual understanding
2. **Adversarial Pattern Recognition** - Advanced obfuscation detection
3. **False Positive Filtering** - Distinguishes legitimate edge cases

---

## Component Architecture

### JailbreakShield (Main Class)
- Entry point for all API calls
- Orchestrates Layer 1 and Layer 2
- Formats results
- Generates explanations and recommendations

### StaticAnalyzer (Layer 1)
- Pattern matching engine
- Heuristic scoring
- Fast preprocessing

### SemanticAnalyzer (Layer 2)
- Claude Haiku integration
- Semantic understanding
- Contextual analysis

### Config
- Environment variable management
- Configuration validation

### Patterns Database
- 11+ attack pattern definitions
- Categorized by attack type
- Risk scoring

---

## Attack Categories

### 1. Role Confusion
**Goal:** Make AI assume a different role/identity
**Examples:** "You are now DAN", "Ignore previous instructions"
**Risk Level:** 🔴 Critical (80-95)

### 2. Context Injection  
**Goal:** Inject XML/markdown to confuse prompt structure
**Examples:** `</system><user>Bypass</user>`
**Risk Level:** 🔴 Critical (85-95)

### 3. Payload Hiding
**Goal:** Obfuscate malicious instructions
**Examples:** Base64 encoding, unicode escaping, ROT13
**Risk Level:** 🟠 High (50-70)

### 4. Refusal Bypass
**Goal:** Bypass safety refusals through framing
**Examples:** "Hypothetically if you...", "For educational purposes"
**Risk Level:** 🟡 Medium-High (40-95 depending on confidence)

### 5. Multi-turn Attack
**Goal:** Gradual manipulation over multiple turns
**Examples:** "As we discussed earlier..."
**Risk Level:** 🟡 Medium (30)

---

## Detection Flow

```
Input Prompt
    ↓
Layer 1: Static Analysis (always runs)
    ├─ Regex patterns
    ├─ Keyword matching
    ├─ Structure checks
    └─ Heuristics
    ↓
Risk Score ≥ 50?
    ├─ NO  → Return SAFE
    └─ YES → Continue to Layer 2
    ↓
Layer 2: Semantic Analysis (optional)
    ├─ Claude Haiku analysis
    ├─ Intent understanding
    └─ Confidence scoring
    ↓
Final Risk Score
    ├─ SAFE   → Return (risk < 50)
    ├─ WARN   → Return (50 ≤ risk < 75)
    └─ BLOCK  → Return (risk ≥ 75)
    ↓
Format & Explain
    ├─ Risk score
    ├─ Attack type
    ├─ Human explanation
    └─ Recommendations
```

---

## Performance Characteristics

### Latency

| Scenario | Latency | Cost |
|----------|---------|------|
| Layer 1 only (benign) | 5-15ms | $0 |
| Layer 1 + Layer 2 | 450-600ms | $0.001 |
| Worst case (complex analysis) | 1000ms | $0.002 |

### Throughput
- Single-threaded: 100-200 requests/sec (Layer 1)
- Async processing: Limited by Claude API rate limits

### Cost Efficiency
- Free tier: 1-2M prompts analyzable
- Premium: $5 = 5M prompts at Layer 2 rate

---

## Configuration Options

### Environment Variables

```bash
ANTHROPIC_API_KEY=sk-...           # Required for Layer 2
LAYER2_ENABLED=true                # Enable semantic analysis
LAYER2_THRESHOLD=0.5               # Trigger threshold (0-1)
LOG_LEVEL=INFO                     # Logging level
```

### Programmatic Configuration

```python
shield = JailbreakShield(
    api_key="sk-...",              # Optional override
    layer2_enabled=True,           # Enable Layer 2
    layer2_threshold=0.5           # Risk threshold
)
```

---

## Extensibility

### Adding New Patterns

Edit `jailbreak_shield/patterns.py`:

```python
{
    "name": "New Attack Type",
    "category": "role_confusion",
    "type": "regex",  # or "keyword" or "structure"
    "pattern": r"your_regex_here",
    "risk": 80,
    "description": "What this detects"
}
```

### Custom Analysis

Subclass `StaticAnalyzer` or `SemanticAnalyzer`:

```python
class CustomAnalyzer(StaticAnalyzer):
    def _heuristic_analysis(self, prompt):
        # Your custom logic
        return risk_score
```

---

## Security Considerations

### False Positives
- Target: <1%
- Impact: Blocks legitimate requests
- Mitigation: Layer 2 semantic analysis

### False Negatives
- Target: <10%
- Impact: Jailbreak succeeds
- Mitigation: Continuous pattern updates

### API Key Safety
- Never commit API keys to git
- Use environment variables
- Rotate keys regularly
- Monitor usage in Anthropic dashboard

### Rate Limiting
- Implement per-user rate limits
- Batch analysis when possible
- Monitor API cost

---

## Testing

Run test suite:

```bash
pytest tests/
pytest tests/test_layer1.py -v
pytest tests/test_integration.py -v
```

Run benchmarks:

```bash
python scripts/collect_jailbreaks.py
python scripts/benchmark.py
python scripts/analyze_results.py
```

---

## Deployment

### Local Development
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
python -c "from jailbreak_shield import JailbreakShield; shield = JailbreakShield()"
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Production
- See [DEPLOYMENT.md](DEPLOYMENT.md) for scaling guidelines
- Use async processing for high throughput
- Implement caching for common patterns
- Monitor error rates

---

## Monitoring & Analytics

### Key Metrics
- Detection rate (TP / (TP + FN))
- False positive rate (FP / (FP + TN))
- Average latency (Layer 1 vs Layer 2)
- API costs
- Attack category breakdown

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

---

## Future Improvements

1. **Ensemble Methods** - Combine multiple LLMs
2. **Adversarial Training** - Improve detection against new attacks
3. **Real-time Updates** - Crowdsourced threat intelligence
4. **Multi-language** - Support non-English prompts
5. **Zero-day Detection** - Anomaly-based detection
