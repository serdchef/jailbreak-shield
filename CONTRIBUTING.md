# Contributing to Jailbreak Shield

Thank you for your interest in contributing to Jailbreak Shield! This document provides guidelines for contributing to the project.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork:** `git clone https://github.com/YOUR_USERNAME/jailbreak-shield.git`
3. **Install dependencies:** `pip install -e ".[dev]"`
4. **Create a branch:** `git checkout -b feature/your-feature`
5. **Make changes and test:** `pytest tests/ -v`
6. **Submit a PR**

## 📋 Development Setup

```bash
# Clone the repository
git clone https://github.com/serdchef/jailbreak-shield.git
cd jailbreak-shield

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v --cov=jailbreak_shield
```

## 🧪 Testing Guidelines

- All new features must include unit tests
- Maintain test coverage above 80%
- Use meaningful test names that describe behavior
- Mock external API calls (e.g., Claude API)

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=jailbreak_shield --cov-report=html

# Run specific test file
pytest tests/test_layer1.py -v
```

## 📝 Code Style

We use **Black** for formatting and **flake8** for linting:

```bash
# Format code
black jailbreak_shield/ --line-length 120

# Check formatting
black --check jailbreak_shield/

# Lint
flake8 jailbreak_shield/ --max-line-length 120
```

## 🔐 Security

- Never commit API keys or secrets
- Run security scans before submitting: `bandit -r jailbreak_shield/`
- Report vulnerabilities via private channels (see SECURITY.md)

## 📦 Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add entry to CHANGELOG if applicable
4. Request review from maintainers

## 🎯 Areas for Contribution

- **Pattern Database:** Add new attack patterns to `jailbreak_shield/patterns.py`
- **Language Support:** Extend multilingual detection
- **Layer Improvements:** Optimize existing layers
- **Documentation:** Improve guides and examples
- **SDK:** Extend Node.js, Python, Go SDKs

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.
