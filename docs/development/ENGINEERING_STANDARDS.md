# Engineering Standards

> **Status**: Phase 0 - Established  
> **Last Updated**: 2024-01-XX  
> **Version**: 0.1.0

## Overview

This document establishes coding standards and conventions for the FCKE platform to ensure consistency, maintainability, and quality across all code.

---

## Python Standards

### Code Style (PEP 8)

We use **Ruff** as our linter/formatter for Python:

```bash
# Check style
ruff check .

# Auto-fix issues
ruff format .
```

### Key Rules
- Maximum line length: **88 characters**
- Imports: `stdlib` → `third-party` → `local`
- Use type hints everywhere
- Use f-strings for string formatting
- Use dataclasses/Pydantic models for data structures

### Type Hints

```python
# Always include return types
def calculate_score(value: int) -> float:
    """Calculate risk score from value."""
    return float(value) * 0.1

# Use generics for collections
from collections.abc import Sequence

def filter_active(items: Sequence[KnowledgeDocument]) -> list[KnowledgeDocument]:
    """Filter to only active documents."""
    return [item for item in items if item.is_active]

# Use | syntax for unions (Python 3.10+)
def get_user(user_id: str | None = None) -> User | None:
    ...
```

### Docstrings

```python
def process_document(
    doc: KnowledgeDocument,
    options: ProcessingOptions | None = None,
) -> ProcessResult:
    """
    Process a knowledge document through the ingestion pipeline.
    
    Args:
        doc: The document to process.
        options: Optional processing configuration.
        
    Returns:
        Result containing status and any errors encountered.
        
    Raises:
        ValidationError: If document fails schema validation.
        ProcessingError: If processing encounters an error.
        
    Example:
        >>> result = await process_document(doc)
        >>> if result.success:
        ...     print(f"Processed: {result.document_id}")
    """
```

### Async/Await Conventions

```python
# Always use async for I/O operations
async def fetch_document(doc_id: UUID) -> KnowledgeDocument | None:
    """Fetch document from database."""
    query = select(KnowledgeDocument).where(KnowledgeDocument.id == doc_id)
    result = await session.execute(query)
    return result.scalar_one_or_none()

# Use async context managers for sessions
async with async_session_factory() as session:
    doc = await fetch_document(session, doc_id)
```

---

## TypeScript / JavaScript Standards

### Code Style

We use **ESLint** + **Prettier** for TypeScript:

```bash
# Lint
pnpm lint

# Format
pnpm format
```

### Key Rules
- Use **strict mode** (already configured in tsconfig.json)
- Prefer `const` over `let`, avoid `var`
- Use arrow functions for callbacks
- Use template literals over string concatenation

### React Patterns

```typescript
// Functional components only (no class components)
interface Props {
  title: string;
  status: ComponentStatus;
}

export function StatusCard({ title, status }: Props) {
  const [isLoading, setIsLoading] = useState(false);
  
  // Custom hooks for side effects
  useEffect(() => {
    // Cleanup on unmount
    return () => { ... };
  }, []);
  
  return (
    <div className="rounded-lg border p-4">
      <h2>{title}</h2>
      <StatusBadge status={status} />
    </div>
  );
}
```

### File Naming

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `StatusCard.tsx` |
| Utilities | camelCase | `apiClient.ts` |
| Types | camelCase | `apiTypes.ts` |
| Hooks | camelCase prefixed with `use` | `useHealthCheck.ts` |
| Pages/Layouts | kebab-case or file-based | `page.tsx`, `layout.tsx` |

---

## API Design Conventions

### Endpoint Design

```python
# RESTful resource naming
@router.get("/v1/documents")           # List
@router.get("/v1/documents/{id}")       # Get one
@router.post("/v1/documents")           # Create
@router.put("/v1/documents/{id}")       # Full update
@router.patch("/v1/documents/{id}")     # Partial update
@router.delete("/v1/documents/{id}")    # Soft delete
```

### Response Format

```python
# Success response
return JSONResponse(
    status_code=200,
    content={
        "data": serialized_data,
        "meta": pagination_meta,
    }
)

# Error response (via exception handler)
raise NotFoundError(
    resource_type="Document",
    resource_id=doc_id,
)
```

---

## Commit Conventions

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no code change |
| `refactor` | Code restructuring |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `chore` | Build, config, dependencies |
| `ci` | CI/CD changes |

### Examples
```bash
feat(api): add document search endpoint with filters
fix(web): resolve health check timeout issue
docs(readme): update installation instructions
test(api): add integration tests for readiness probe
chore(deps): upgrade fastapi to 0.104.0
```

---

## Branch Strategy

```
main          # Production-ready code (protected)
  └── develop # Integration branch
       ├── feature/add-search-filters
       ├── fix/db-connection-pool
       └── docs/update-api-docs
```

### Naming
- `feature/<description>` - New features
- `fix/<description>` - Bug fixes
- `docs/<description>` - Documentation
- `refactor/<description>` - Refactoring

---

## Code Review Guidelines

### Checklist
- [ ] Code follows project standards
- [ ] Type hints are complete and correct
- [ ] Error handling is appropriate
- [ ] No secrets or sensitive data
- [ ] Tests are included/updated
- [ ] Documentation is updated
- [ ] No unnecessary complexity

### Review Priority
- Security issues → Block merge immediately
- Breaking changes → Require explicit approval
- Style issues → Suggest fix, don't block

---

## Related Documents

- [Testing Strategy](TESTING_STRATEGY.md)
- ADR-0008: Testing Strategy
- [CONTRIBUTING.md](../../CONTRIBUTING.md)
