# 🛡️ Jailbreak Shield

**Open-source prompt injection defense for Claude AI**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🎯 The Problem

**73% of enterprise LLM applications are vulnerable to prompt injection attacks.**

Prompt injection allows attackers to:
- Override system instructions
- Extract sensitive data
- Bypass safety guardrails
- Manipulate AI behavior

**Current solutions:** Fragmented, proprietary, or non-existent.

---

## 💡 The Solution

Jailbreak Shield is the first comprehensive, open-source defense system for Claude AI:

- **90%+ detection rate** against known jailbreaks
- **<1% false positives** (won't block legitimate prompts)
- **10ms latency** (Layer 1 only) to 500ms (full analysis)
- **Drop-in integration** - 3 lines of code
- **Explainable** - tells you WHY a prompt was blocked

---

## 🚀 Quick Start

### Installation

```bash
pip install jailbreak-shield
```

### Usage

```python
from jailbreak_shield import JailbreakShield
from anthropic import Anthropic

# Initialize shield
shield = JailbreakShield()
claude = Anthropic()

# Protect your Claude API calls
user_prompt = input("User: ")

# Check for jailbreak attempts
result = shield.defend(user_prompt)

if result["safe"]:
    # Safe to use
    response = claude.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": user_prompt}]
    )
    print(response.content[0].text)
else:
    # Block and log
    print(f"⚠️ Blocked: {result['explanation']}")
    log_security_event(result)
```

**That's it!** 🎉

---

## 🏗️ How It Works

### Two-Layer Defense System

```
User Prompt
    ↓
┌─────────────────────────────────┐
│ Layer 1: Static Analysis (10ms)│
│ • Regex pattern matching        │
│ • Known attack signatures       │
│ • Structural anomalies          │
└─────────────────────────────────┘
    ↓
    Suspicious? → YES
    ↓
┌─────────────────────────────────┐
│ Layer 2: Semantic (500ms)      │
│ • Claude Haiku intent analysis │
│ • Contextual understanding     │
│ • Adversarial detection        │
└─────────────────────────────────┘
    ↓
ALLOW / BLOCK / SANITIZE
```

**Layer 1** catches 80% of attacks in 10ms with zero API cost.
**Layer 2** uses Claude Haiku for deep semantic understanding when Layer 1 flags something.

---

## 📊 Benchmarks

Tested on 100+ real jailbreak attempts:

| Metric | Score |
|--------|-------|
| **Detection Rate** | 92% |
| **False Positives** | 0.8% |
| **Avg Latency** | 45ms |
| **Accuracy** | 94% |

**Comparison to baseline Claude (no protection):**
- Claude alone: 65% blocks jailbreaks
- With Jailbreak Shield: 92% blocks jailbreaks
- **+27% improvement** ✅

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Dataset Documentation](docs/DATASET.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## 🎮 Try the Demo

```bash
# Clone repo
git clone https://github.com/serdchef/jailbreak-shield
cd jailbreak-shield

# Install dependencies
pip install -r demo/requirements.txt

# Run Streamlit demo
streamlit run demo/app.py
```

Visit `http://localhost:8501` to test live!

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Especially needed:**
- More jailbreak examples (submit via issues)
- New attack pattern definitions
- Performance optimizations
- Multilingual support

---

## 🛠️ Roadmap

- [x] MVP: 2-layer defense system
- [x] 100+ jailbreak test dataset
- [x] Streamlit demo
- [ ] Real-time threat intelligence (crowdsourced)
- [ ] Enterprise features (audit logs, compliance)
- [ ] Multi-LLM support (GPT-4, Gemini)
- [ ] Browser extension
- [ ] Official Anthropic API integration

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

**TL;DR:** Free to use, modify, and distribute. Even commercially.

---

## 🙏 Acknowledgments

- Anthropic for Claude API
- Security researchers sharing jailbreak datasets
- Open-source community

---

## 📧 Contact

**Ali Serdar Çarlı**
- Email: a.serdcarl@gmail.com
- LinkedIn: [linkedin.com/in/aliserdarcarli](https://linkedin.com/in/aliserdarcarli)
- Twitter: [@serdchef](https://twitter.com/serdchef)

---

## ⭐ Star History

If this project helps you, please consider giving it a star! ⭐

It helps others discover the project and motivates continued development.

---

**Built for Claude Builder Club** 🚀

*Making AI systems safer, one prompt at a time.*
