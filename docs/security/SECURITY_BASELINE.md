# Security Baseline

> **Status**: Phase 0 - Foundation  
> **Last Updated**: 2024-01-XX  
> **Version**: 0.1.0

## Overview

This document establishes the security baseline for the Financial Crime Knowledge Engine. Security is critical given the sensitive nature of financial crime data.

---

## Current Security Posture (Phase 0)

### What's Implemented
| Measure | Status | Notes |
|---------|--------|-------|
| No hardcoded secrets | ✅ Verified | .env.example only |
| Input validation framework | ✅ SCAFFOLDED | Pydantic models defined |
| SQL injection protection | ✅ IMPLEMENTED | SQLAlchemy parameterized queries |
| CORS configuration | ✅ IMPLEMENTED | Configurable origins |
| Security headers (web) | ✅ IMPLEMENTED | X-Frame-Options, etc. |
| .gitignore for secrets | ✅ IMPLEMENTED | Comprehensive rules |

### What's Planned
| Measure | Target Phase | Priority |
|---------|--------------|----------|
| Authentication | Phase 1 | High |
| Authorization/RBAC | Phase 1 | High |
| Rate limiting | Phase 1 | Medium |
| Audit logging (full) | Phase 1 | High |
| Encryption at rest | Phase 2 | Medium |
| AI security guardrails | Phase 2 | High |

---

## Secret Management

### Principles
1. **Never commit secrets** to version control
2. **Use environment variables** for all secrets
3. **Rotate credentials** regularly
4. **Use different keys** per environment

### Current Implementation (Phase 0)
```bash
# All config via environment variables
DATABASE_URL=postgresql+asyncpg://...
REDIS_URL=redis://...

# Secrets managed externally (Phase 1+)
# SECRET_KEY=...           # From Vault/Secrets Manager
# ENCRYPTION_KEY=...       # From Vault/Secrets Manager
```

### Planned Enhancement (Phase 1)
- HashiCorp Vault or AWS Secrets Manager integration
- Automatic secret rotation
- Secret scanning in CI/CD

---

## Input Validation Strategy

### API Layer (FastAPI + Pydantic)

```python
# Example: Validated request model
class DocumentSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    document_type: DocumentType | None = None
    page: int = Field(default=1, ge=1, le=1000)
    page_size: int = Field(default=20, ge=1, le=100)
```

### Validation Rules
| Input Type | Validation |
|------------|-----------|
| Strings | Length limits, allowlist patterns |
| Numbers | Range checks, type coercion |
| Dates | ISO format, range validation |
| UUIDs | Format validation |
| JSON | Schema validation |
| File uploads | Size limits, type checking |

### SQL Injection Prevention
- ✅ Always use SQLAlchemy ORM (parameterized queries)
- ✅ Never concatenate user input into SQL strings
- ✅ Use raw SQL only with explicit parameter binding

---

## Authentication & Authorization (Planned - Phase 1)

See [Authentication & Authorization](AUTHENTICATION_AUTHORIZATION.md) for full details.

---

## AI Security Boundaries (Planned - Phase 2)

### Data Flow Controls
```
User Query → [Sanitization] → LLM Provider → [Filter] → Response
                    ↓                                    ↓
              Audit Log                              Safety Check
```

### Guardrails
- Prompt injection detection
- Output content filtering
- PII redaction before external APIs
- Rate limiting per user/session

---

## Security Headers (Web)

Currently implemented in Next.js:

| Header | Value | Purpose |
|--------|-------|---------|
| X-Frame-Options | DENY | Prevent clickjacking |
| X-Content-Type-Options | nosniff | MIME sniffing prevention |
| Referrer-Policy | strict-origin-when-cross-origin | Control referrer info |
| X-XSS-Protection | 1; mode=block | XSS filter |

### Planned Additions (Phase 1)
| Header | Value | Purpose |
|--------|-------|---------|
| Strict-Transport-Security | max-age=31536000; includeSubDomains | HTTPS enforcement |
| Content-Security-Policy | (defined) | Resource loading control |
| Permissions-Policy | (defined) | Browser feature control |

---

## Dependency Security

### Current Practices
- ✅ Dependabot enabled (GitHub)
- ✅ Regular dependency updates
- ✅ `pnpm audit` in CI pipeline

### Planned Enhancements
- Automated security patching (critical)
- SBOM (Software Bill of Materials) generation
- License compliance checking

---

## Incident Response (Framework)

### Severity Levels
| Level | Definition | Response Time |
|-------|-----------|---------------|
| Critical | Active exploitation, data breach | Immediate (< 1 hour) |
| High | Vulnerability with exploit available | < 24 hours |
| Medium | Vulnerability no known exploit | < 7 days |
| Low | Best practice improvement | Next release |

### Contact (To Be Defined)
- Security email: security@fcke.example.com
- PGP key: (to be published)
- Bug bounty: (Phase 3 consideration)

---

## Compliance Considerations

The FCKE platform may need to comply with:
- SOC 2 Type II (for enterprise customers)
- GDPR (if processing EU personal data)
- Financial regulations (depending on deployment context)

---

## Related Documents

- [Authentication & Authorization](AUTHENTICATION_AUTHORIZATION.md)
- ADR-0005: Authentication Strategy
- ADR-0010: Observability Strategy
