# 📑 JAILBREAK SHIELD - DOCUMENTATION INDEX

## 🎯 Navigation Guide

### 🚀 Getting Started (Pick Your Path)

#### ⏱️ 5 Minutes?
→ [QUICKSTART.md](QUICKSTART.md)
**Install, configure, and run in 5 minutes**

#### ⏱️ 15 Minutes?
→ [START_HERE.md](START_HERE.md)
**Comprehensive overview and next steps**

#### ⏱️ 30 Minutes?
→ [README.md](README.md)
**Full feature overview with examples**

#### ⏱️ Full Deep Dive?
→ [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
**Complete implementation details**

---

## 📚 By Use Case

### "I Want to Use Jailbreak Shield in My App"
1. Read [QUICKSTART.md](QUICKSTART.md)
2. Review [docs/API.md](docs/API.md)
3. Check examples in [docs/API.md#examples](docs/API.md)
4. See integration example in [README.md](README.md)

### "I Want to Understand How It Works"
1. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. Review [jailbreak_shield/shield.py](jailbreak_shield/shield.py) code
3. Check attack patterns in [jailbreak_shield/patterns.py](jailbreak_shield/patterns.py)
4. See layer explanations in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

### "I Want to Deploy to Production"
1. Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. Review security section in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
3. Check monitoring setup in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
4. See cost optimization in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

### "I Want to Test It Out"
1. Run [QUICKSTART.md](QUICKSTART.md) steps
2. Execute `pytest tests/`
3. Try `streamlit run demo/app.py`
4. Test with examples in [data/jailbreaks.csv](data/jailbreaks.csv)

### "I Want to Research the Patterns"
1. Read [docs/DATASET.md](docs/DATASET.md)
2. Review [jailbreak_shield/patterns.py](jailbreak_shield/patterns.py)
3. Check examples in [data/jailbreaks.csv](data/jailbreaks.csv)
4. Run `python scripts/analyze_results.py`

---

## 📄 Complete File Index

### Root Documentation

| File | Purpose | Read Time |
|------|---------|-----------|
| [START_HERE.md](START_HERE.md) | Quick navigation & overview | 10 min |
| [README.md](README.md) | Main project documentation | 15 min |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide | 5 min |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | Full implementation details | 20 min |
| [COMPLETION_REPORT.md](COMPLETION_REPORT.md) | Project completion report | 15 min |
| [FILE_MANIFEST.md](FILE_MANIFEST.md) | Complete file listing | 10 min |
| [INDEX.md](INDEX.md) | This file - Documentation index | 5 min |

### Core Library

| File | Type | Purpose |
|------|------|---------|
| [jailbreak_shield/__init__.py](jailbreak_shield/__init__.py) | Python | Package initialization |
| [jailbreak_shield/shield.py](jailbreak_shield/shield.py) | Python | Main JailbreakShield class |
| [jailbreak_shield/layer1_static.py](jailbreak_shield/layer1_static.py) | Python | Layer 1 pattern analysis |
| [jailbreak_shield/layer2_semantic.py](jailbreak_shield/layer2_semantic.py) | Python | Layer 2 semantic analysis |
| [jailbreak_shield/patterns.py](jailbreak_shield/patterns.py) | Python | Attack pattern database |
| [jailbreak_shield/config.py](jailbreak_shield/config.py) | Python | Configuration management |

### Documentation

| File | Purpose | Audience |
|------|---------|----------|
| [docs/API.md](docs/API.md) | Complete API reference | Developers |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture deep dive | Architects, Researchers |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide | DevOps, Operations |
| [docs/DATASET.md](docs/DATASET.md) | Dataset structure & ethics | Data Scientists, Researchers |
| [docs/DEMO.md](docs/DEMO.md) | Demo application guide | End Users |

### Testing

| File | Purpose | Coverage |
|------|---------|----------|
| [tests/test_layer1.py](tests/test_layer1.py) | Layer 1 unit tests | Static analysis |
| [tests/test_layer2.py](tests/test_layer2.py) | Layer 2 unit tests | Semantic analysis |
| [tests/test_integration.py](tests/test_integration.py) | Integration tests | Full pipeline |

### Scripts

| File | Purpose | Usage |
|------|---------|-------|
| [scripts/collect_jailbreaks.py](scripts/collect_jailbreaks.py) | Collect examples | `python scripts/collect_jailbreaks.py` |
| [scripts/test_claude.py](scripts/test_claude.py) | Test against Claude | `python scripts/test_claude.py` |
| [scripts/benchmark.py](scripts/benchmark.py) | Run benchmarks | `python scripts/benchmark.py` |
| [scripts/analyze_results.py](scripts/analyze_results.py) | Analyze results | `python scripts/analyze_results.py` |

### Demo Application

| File | Purpose |
|------|---------|
| [demo/app.py](demo/app.py) | Streamlit web interface |
| [demo/requirements.txt](demo/requirements.txt) | Demo dependencies |
| [demo/README.md](demo/README.md) | Demo documentation |

### Configuration

| File | Purpose |
|------|---------|
| [setup.py](setup.py) | Package configuration |
| [requirements.txt](requirements.txt) | Dependencies |
| [.env.example](.env.example) | Environment variables template |
| [.gitignore](.gitignore) | Git ignore rules |
| [LICENSE](LICENSE) | MIT License |

### Data

| File | Purpose |
|------|---------|
| [data/jailbreaks.csv](data/jailbreaks.csv) | Test examples |
| [data/patterns.json](data/patterns.json) | Attack patterns |

---

## 🔍 Find What You Need

### By Question

**Q: How do I install Jailbreak Shield?**
→ [QUICKSTART.md](QUICKSTART.md#step-1-install-dependencies)

**Q: How do I use it in my code?**
→ [docs/API.md#examples](docs/API.md#examples)

**Q: How does the detection work?**
→ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

**Q: How do I deploy to production?**
→ [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

**Q: What attacks does it detect?**
→ [docs/ARCHITECTURE.md#attack-categories](docs/ARCHITECTURE.md#attack-categories)

**Q: What are the performance metrics?**
→ [IMPLEMENTATION_SUMMARY.md#benchmarks](IMPLEMENTATION_SUMMARY.md#benchmarks)

**Q: How do I run the tests?**
→ [QUICKSTART.md#running-tests](QUICKSTART.md#running-tests)

**Q: How do I try the interactive demo?**
→ [QUICKSTART.md#demo](QUICKSTART.md#demo)

**Q: What data is included?**
→ [docs/DATASET.md](docs/DATASET.md)

**Q: Is there a cost?**
→ [README.md#free-tier](README.md) / [docs/DEPLOYMENT.md#cost-optimization](docs/DEPLOYMENT.md#cost-optimization)

---

## 🎓 Learning Paths

### Path 1: Quick Integration (30 minutes)
1. [QUICKSTART.md](QUICKSTART.md) - Setup
2. [docs/API.md#examples](docs/API.md#examples) - Code examples
3. Try in your own code
4. Done! 🎉

### Path 2: Understanding the System (2 hours)
1. [README.md](README.md) - Overview
2. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Design
3. [docs/API.md](docs/API.md) - API reference
4. Review code in [jailbreak_shield/](jailbreak_shield/)
5. Run tests: `pytest tests/`

### Path 3: Production Deployment (3 hours)
1. [QUICKSTART.md](QUICKSTART.md) - Local setup
2. [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment options
3. Review [docs/DEPLOYMENT.md#security-best-practices](docs/DEPLOYMENT.md#security-best-practices)
4. Configure monitoring & logging
5. Deploy to your platform

### Path 4: Research & Customization (4+ hours)
1. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Deep dive
2. [docs/DATASET.md](docs/DATASET.md) - Data structure
3. Review [jailbreak_shield/patterns.py](jailbreak_shield/patterns.py)
4. Run [scripts/benchmark.py](scripts/benchmark.py)
5. Customize patterns as needed

---

## 🗂️ File Organization Strategy

### If You're New
Start → [START_HERE.md](START_HERE.md)
Then → [QUICKSTART.md](QUICKSTART.md)
Then → [README.md](README.md)

### If You Want to Integrate
Focus → [docs/API.md](docs/API.md)
And → Code examples in API docs
Test → [tests/](tests/) for patterns

### If You Want to Deploy
Focus → [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
And → Security section
And → Monitoring setup

### If You Want to Understand Everything
Read → [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
Then → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
Then → Review code in [jailbreak_shield/](jailbreak_shield/)

---

## 📊 Documentation Statistics

| Category | Count | Size |
|----------|-------|------|
| Root Docs | 7 | 500+ lines |
| API Docs | 5 | 2,000+ lines |
| Code | 19 | 3,800+ lines |
| Tests | 3 | 300 lines |
| Scripts | 4 | 500+ lines |
| Total | 33+ | 7,100+ lines |

---

## 🔗 Quick Links

### Essential
- [START_HERE.md](START_HERE.md) - Start here
- [README.md](README.md) - Main docs
- [QUICKSTART.md](QUICKSTART.md) - Quick setup

### API & Usage
- [docs/API.md](docs/API.md) - API reference
- [jailbreak_shield/shield.py](jailbreak_shield/shield.py) - Main code

### Deployment & Ops
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy to prod
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design

### Data & Research
- [docs/DATASET.md](docs/DATASET.md) - Data info
- [jailbreak_shield/patterns.py](jailbreak_shield/patterns.py) - Patterns

### Testing & Demo
- [docs/DEMO.md](docs/DEMO.md) - Demo app
- [tests/](tests/) - Test suite

---

## 💡 Tips for Navigating

1. **Use Ctrl+F** to search within markdown files
2. **Start with [START_HERE.md](START_HERE.md)** if you're unsure where to begin
3. **Each document** is self-contained and can be read independently
4. **Code examples** are in [docs/API.md](docs/API.md)
5. **Deployment help** is in [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## 📞 Need Help?

| Question | Where to Look |
|----------|---------------|
| How to start? | [START_HERE.md](START_HERE.md) |
| Quick setup? | [QUICKSTART.md](QUICKSTART.md) |
| API usage? | [docs/API.md](docs/API.md) |
| How it works? | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Deployment? | [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| Data info? | [docs/DATASET.md](docs/DATASET.md) |
| Demo guide? | [docs/DEMO.md](docs/DEMO.md) |
| Full details? | [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) |

---

**Happy exploring! 🚀**

For questions, check the relevant documentation file.

For code, review [jailbreak_shield/](jailbreak_shield/) or [tests/](tests/).

For examples, see [scripts/](scripts/) or [docs/API.md](docs/API.md#examples).
