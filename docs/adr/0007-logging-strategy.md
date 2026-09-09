# ADR-0007: Logging Strategy

## Status

**Accepted** | 2024-01-XX

## Context

Effective logging is critical for:
- Debugging issues in production
- Security auditing and compliance
- Performance monitoring
- Understanding user behavior

## Decision

### Structured Logging with structlog

#### Log Format (Production - JSON)
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "event": "document_created",
  "logger": "app.api.v1.documents",
  "document_id": "uuid-here",
  "user_id": "user-123",
  "duration_ms": 45.2,
  "request_id": "req-abc"
}
```

#### Log Format (Development - Human-readable)
```
10:30:00 [INFO] document_created {document_id: uuid, duration_ms: 45.2}
```

### Log Levels Usage
| Level | When to Use |
|-------|-------------|
| DEBUG | Detailed development info |
| INFO | Normal operations (requests, job starts) |
| WARNING | Recoverable issues, deprecations |
| ERROR | Failures that need investigation |
| CRITICAL | System-level failures |

### What to Log
**Always:**
- Timestamp
- Log level
- Event name
- Request/correlation ID
- User/actor ID (when available)

**Sometimes:**
- Duration/timing data
- Key entity IDs
- Error details (sanitized)

**Never:**
- Passwords or secrets
- Full request bodies (PII)
- Credit card numbers
- Raw stack traces in production

## Alternatives Considered

### Option A: Python logging module only
- Built-in, simple
- Less structured output
- Harder to parse at scale

### Option B: structlog with JSON output (CHOSEN)
- Structured from the start
- Easy to parse with log aggregators
- Context propagation built-in
- Development-friendly console output

## Consequences

### Positive
- Searchable, parseable logs
- Consistent format across services
- Good tooling support (ELK, Datadog, etc.)
- Context propagation for distributed tracing

### Negative
- Additional dependency
- Need to configure properly for each environment

## Implementation Status
- ✅ Phase 0: Basic structlog setup in API
- 🟡 Phase 1+: Correlation IDs, sampling, log aggregation

## Related Decisions

- [ADR-0010: Observability Strategy](0010-observability-strategy.md)
