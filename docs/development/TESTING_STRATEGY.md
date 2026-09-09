# Testing Strategy

> **Status**: Phase 0 - Foundation  
> **Last Updated**: 2024-01-XX  
> **Version**: 0.1.0

## Overview

This document defines the testing strategy for the FCKE platform, including test types, coverage expectations, and conventions.

---

## Testing Pyramid

```
                    ╱╲
                   ╱  ╲         E2E Tests
                  ╱────╲        (Critical paths only)
                 ╱      ╲
                ╱────────╲     Integration Tests
               ╱          ╲    (API contracts, DB)
              ╱            ╲
             ╱──────────────╲  Unit Tests
            ╱                ╲ (Business logic)
           ╱──────────────────╲
```

### Test Distribution Targets

| Test Type | Target % | Current (Phase 0) |
|-----------|----------|-------------------|
| Unit Tests | 60% | ~30% |
| Integration Tests | 30% | ~10% |
| E2E Tests | 10% | 0% |

---

## Test Types & Tools

### 1. Unit Tests

**Purpose**: Test individual functions/classes in isolation.

**Tools**:
- Python: `pytest` with `pytest-asyncio`
- TypeScript: `vitest`

**What to Test**:
- Business logic functions
- Utility functions
- Data transformations
- Validation logic

**What NOT to Test**:
- External services (mock them)
- Database queries (integration test instead)
- Framework code

#### Example (Python)
```python
def test_calculate_risk_score_high_value():
    """Given high transaction amount, when calculating risk, then return high score."""
    transaction = Transaction(amount=1000000, country="HIGH_RISK")
    score = calculate_risk_score(transaction)
    assert score >= 80


def test_document_status_transition():
    """Given pending document, when processing completes, status becomes active."""
    doc = KnowledgeDocument(status=DocumentStatus.PENDING)
    doc.mark_processed()
    assert doc.status == DocumentStatus.ACTIVE
```

#### Example (TypeScript)
```typescript
describe("API Client", () => {
  it("should construct correct URL", () => {
    const client = new ApiClient("http://localhost:8000");
    expect(client.baseUrl).toBe("http://localhost:8000");
  });

  it("should parse error response correctly", () => {
    const error = parseErrorResponse({ status: 404, data: { detail: "Not found" } });
    expect(error.code).toBe("NOT_FOUND");
  });
});
```

---

### 2. Integration Tests

**Purpose**: Test component interactions.

**Tools**:
- Python: `pytest` + `httpx` + `test database`
- TypeScript: `vitest` + MSW (Mock Service Worker)

**What to Test**:
- API endpoint contracts
- Database operations
- External service integrations (with test doubles)

#### Example (Python - API Test)
```python
@pytest.mark.asyncio
async def test_health_endpoint_returns_200():
    """Given running API, when GET /health, then return 200 with healthy status."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
```

---

### 3. End-to-End Tests (Planned - Phase 1+)

**Purpose**: Test complete user journeys.

**Tool**: Playwright

**What to Test**:
- User login flow
- Document search flow
- Assessment creation workflow
- Critical business processes

---

## Coverage Requirements

### Minimum Thresholds

| Component | Line Coverage | Branch Coverage |
|-----------|--------------|-----------------|
| Core domain logic | > 90% | > 85% |
| API endpoints | > 80% | > 75% |
| Utility functions | > 85% | > 80% |
| Configuration | > 70% | N/A |
| Overall project | > 75% | > 70% |

### Exclusions from Coverage
- `__init__.py` files
- Migration files
- Test files themselves
- Auto-generated code
- Abstract base classes (implementation only)

---

## Test Naming Conventions

### Python (pytest)
```python
# Format: test_{unit}_{behavior}_{expected_result}
def test_health_endpoint_returns_healthy_status():
    ...

def test_health_endpoint_includes_version_field():
    ...

def test_readiness_probe_fails_when_db_unavailable():
    ...
```

### TypeScript (vitest)
```typescript
// Format: describe what, it should behavior
describe("Health Check API", () => {
  it("should return healthy status", async () => { ... });
  
  it("should include version information", async () => { ... });
});
```

---

## Test Data Management

### Fixtures
Use pytest fixtures for common test data:

```python
@pytest.fixture
async def sample_document():
    return KnowledgeDocument(
        title="Test Regulation",
        document_type=DocumentType.REGULATION,
        status=DocumentStatus.ACTIVE,
    )

@pytest.fixture
async def db_session():
    # Setup: Create test database session
    async with async_test_session() as session:
        yield session
        # Teardown: Rollback changes
```

### Principles
1. **Isolation**: Each test should be independent
2. **Determinism**: Same result on every run
3. **Speed**: Tests should run quickly
4. **Clarity**: Test name explains the scenario

---

## Running Tests

### Commands
```bash
# Backend tests
cd apps/api && pytest tests/ -v

# Frontend tests  
pnpm --filter @fcke/web test

# All tests
pnpm test

# With coverage
pnpm test:coverage
```

### CI/CD Integration
Tests run automatically on:
- Every pull request
- Merge to main branch
- Nightly schedule (full suite)

---

## Implementation Status (Phase 0)

| Capability | Status |
|------------|--------|
| Test structure | ✅ SCAFFOLDED |
| Health endpoint tests | ✅ IMPLEMENTED |
| Basic unit test examples | ✅ IMPLEMENTED |
| Test configuration | ✅ IMPLEMENTED |
| E2E tests | ⚪ PLANNED |
| Coverage reporting | ⚪ PLANNED |
| Performance tests | ⚪ PLANNED |

---

## Related Documents

- ADR-0008: Testing Strategy
- [Engineering Standards](ENGINEERING_STANDARDS.md)
- [Implementation Status](IMPLEMENTATION_STATUS.md)
