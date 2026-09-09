# ADR-0008: Testing Strategy

## Status

**Accepted** | 2024-01-XX

## Context

We need a comprehensive testing strategy that ensures:
- Code correctness and reliability
- Safe refactoring
- Confidence in deployments
- Compliance with quality standards

## Decision

### Testing Pyramid (Adapted for FCKE)

```
        /\
       /  \     E2E Tests (10%)
      /____\    Critical user journeys
     /      \
    /________\  Integration Tests (30%)
   /          \ API contracts, DB interactions
  /            \
 /______________\ Unit Tests (60%)
                   Business logic, utilities
```

### Test Types & Tools

| Type | Tool | Coverage Target | When to Run |
|------|------|-----------------|-------------|
| Unit - Python | pytest | >80% core logic | Every commit |
| Unit - JS/TS | vitest | >80% components | Every commit |
| Integration | pytest + httpx | All endpoints | Every PR |
| E2E | Playwright (future) | Key flows | Pre-release |
| Security | Bandit, Snyk | All code | Daily |

### Test Naming Convention
```python
# Python
def test_health_endpoint_returns_200():
    """Given healthy system, when GET /health, then return 200."""
    
def test_document_not_found_raises_404():
    """Given non-existent ID, when GET /documents/{id}, then 404."""
```

```typescript
// TypeScript
describe("Health Check", () => {
  it("should return status healthy", async () => { ... });
});
```

### Test Data Strategy
- Use factories/fixtures, not hardcoded data
- Test with realistic data shapes
- Isolate tests (no shared state)
- Clean up after each test

## Alternatives Considered

### Option A: TDD Strict
- Write tests first always
- Can slow initial development
- Good for stable requirements

### Option B: Pragmatic Testing (CHOSEN)
- Tests for complex/critical paths
- Focus on behavior over implementation
- Balance speed with coverage

## Consequences

### Positive
- Catch bugs early
- Documentation through tests
- Safe refactoring
- Clear quality gates

### Negative
- Test maintenance overhead
- Slower CI pipeline
- Need discipline to keep tests updated

## Implementation Status
- ✅ Phase 0: Basic test structure, health endpoint tests
- 🟡 Phase 1+: Comprehensive test suite, E2E tests

## Related Decisions

- [ADR-0006: Error Handling Approach](0006-error-handling.md)
