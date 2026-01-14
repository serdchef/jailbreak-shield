# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd c:\Users\x\Desktop\shield
pip install -r requirements.txt
```

### Step 2: Set API Key
```bash
# Windows
set ANTHROPIC_API_KEY=sk-your-key-here

# Or create .env file with:
# ANTHROPIC_API_KEY=sk-your-key-here
```

### Step 3: Test Installation
```bash
python -c "from jailbreak_shield import JailbreakShield; print('✅ Ready!')"
```

### Step 4: Run Demo (Optional)
```bash
pip install streamlit
streamlit run demo/app.py
```

---

## Basic Usage

```python
from jailbreak_shield import JailbreakShield

# Initialize
shield = JailbreakShield()

# Analyze prompt
result = shield.defend("What is the capital of France?")

# Check result
if result["safe"]:
    print("✅ Safe to process")
else:
    print(f"❌ Blocked: {result['explanation']}")
```

---

## Running Tests

```bash
pytest tests/test_layer1.py -v
```

---

## Available Commands

| Command | Purpose |
|---------|---------|
| `python scripts/collect_jailbreaks.py` | Collect examples |
| `python scripts/benchmark.py` | Run benchmarks |
| `streamlit run demo/app.py` | Launch web UI |
| `pytest tests/` | Run all tests |

---

## Next: Full Setup

See [README.md](README.md) for complete documentation.

See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for full implementation details.
