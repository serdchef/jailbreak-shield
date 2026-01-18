# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 3.x.x   | :white_check_mark: |
| 2.x.x   | :x:                |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in Jailbreak Shield, please report it responsibly:

1. **DO NOT** create a public GitHub issue
2. Email: a.serdcarl@gmail.com with subject "SECURITY: Jailbreak Shield"
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to resolve the issue.

## Security Best Practices

### API Key Management

```bash
# Use environment variables, never hardcode
export ANTHROPIC_API_KEY="your-key-here"

# Or use .env file (added to .gitignore)
echo "ANTHROPIC_API_KEY=your-key-here" > .env
```

### Vercel Environment Variables

1. Go to Vercel Dashboard → Project → Settings → Environment Variables
2. Add `ANTHROPIC_API_KEY` as encrypted secret
3. Rotate keys periodically (recommended: every 90 days)

### Rate Limiting

Enable rate limiting in production:

```python
shield = JailbreakShield(
    rate_limit_enabled=True,
    rate_limit_rpm=60  # Requests per minute
)
```

### Logging & PII

The logger masks sensitive data by default:

```python
# Automatically masks:
# - IP addresses
# - Email addresses
# - API keys
# - Credit card patterns
```

## Secrets Rotation Schedule

| Secret | Rotation Frequency | Last Rotated |
|--------|-------------------|--------------|
| ANTHROPIC_API_KEY | 90 days | On deployment |
| Vercel Token | 180 days | Manual |

## Security Audits

- Static analysis: Bandit (automated in CI)
- Dependency scanning: Dependabot (GitHub)
- Manual review: On major releases
