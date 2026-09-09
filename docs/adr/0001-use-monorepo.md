# ADR-0001: Use Monorepo Structure

## Status

**Accepted** | 2024-01-XX

## Context

The Financial Crime Knowledge Engine consists of multiple components:
- Web frontend (Next.js)
- API backend (FastAPI)
- Background worker (Python)
- Shared packages (UI components, SDK, utilities)

We need to decide on a repository structure that supports coordinated development across these components while maintaining clear separation of concerns.

## Decision

**Use a monorepo structure with pnpm workspaces for JavaScript/TypeScript and co-located Python projects.**

```
financial-crime-knowledge-engine/
├── apps/           # Deployable applications
│   ├── web/        # Next.js frontend
│   ├── api/        # FastAPI backend
│   └── worker/     # Python worker
├── packages/       # Shared libraries
│   ├── ui/
│   ├── knowledge/
│   ├── sdk/
│   └── shared/
└── ...
```

## Alternatives Considered

### Option A: Multiple Separate Repositories
- **Pros**: Clear isolation, independent CI/CD, per-repo access control
- **Cons**: Versioning complexity, difficult atomic commits, dependency hell
- **Verdict**: Rejected - too complex for our team size and coordination needs

### Option B: Monorepo with Nx/Turborepo
- **Pros**: Advanced caching, affected build detection, task graph
- **Cons**: Learning curve, additional tooling complexity
- **Verdict**: Not chosen for Phase 0 - can migrate later if needed

### Option C: Simple Monorepo with pnpm workspaces (CHOSEN)
- **Pros**: Simple setup, good TypeScript support, industry standard
- **Cons**: Basic tooling, may need enhancement later
- **Verdict**: Selected for simplicity and adequacy for Phase 0

## Consequences

### Positive
- Single source of truth for all code
- Atomic changes across frontend/backend/shared code
- Shared tooling configuration
- Simplified dependency management within JS/TS ecosystem
- Easy to onboard new developers

### Negative
- Larger repository size
- All changes in one place (can be noisy)
- Need to be careful about coupling between apps
- Python not managed by pnpm (separate tooling needed)

## Related Decisions

- [ADR-0002: Technology Stack Selection](0002-technology-stack.md)
- [ADR-009: Container Strategy](0009-container-strategy.md)
