# ADR-0002: Technology Stack Selection

## Status

**Accepted** | 2024-01-XX

## Context

We need to select the core technology stack for the Financial Crime Knowledge Engine that will serve us through Phase 0 and beyond.

## Decision

### Frontend Stack
| Technology | Version | Rationale |
|------------|---------|-----------|
| Next.js | 15+ | React meta-framework with SSR/SSG, App Router, great DX |
| React | 19+ | Industry-standard UI library with hooks and concurrent features |
| TypeScript | 5+ | Type safety for large codebases |
| Tailwind CSS | 4+ | Utility-first CSS, fast development |
| shadcn/ui | - | High-quality, customizable component library |

### Backend Stack
| Technology | Version | Rationale |
|------------|---------|-----------|
| Python | 3.11+ | Data science ecosystem, async support |
| FastAPI | 0.115+ | Modern async API framework, OpenAPI auto-generation |
| Pydantic v2 | 2.10+ | Data validation, settings management |
| SQLAlchemy 2.0 | 2.0+ | Mature async ORM for Python |
| Alembic | - | Database migration tool |

### Infrastructure
| Technology | Rationale |
|------------|-----------|
| PostgreSQL 16 | Robust relational database with JSONB, full-text search |
| Redis 7 | Caching, job queue broker |
| Docker | Containerization for consistent environments |
| GitHub Actions | CI/CD (free for open source) |

## Alternatives Considered

### Frontend Alternatives
- **Vue/Nuxt**: Good alternative but smaller ecosystem
- **Svelte/SvelteKit**: Interesting but less enterprise adoption
- **Angular**: Too opinionated for our needs

### Backend Alternatives
- **Node.js/Express**: Considered but Python better for AI/ML integration
- **Django REST Framework**: More batteries-included but less flexible
- **Go/Fiber**: Great performance but less data science tooling

## Consequences

### Positive
- Strong type safety across stack
- Excellent developer experience
- Large ecosystems and community support
- Well-documented technologies
- Easy to hire developers with these skills

### Negative
- Two language ecosystems to manage
- Need expertise in both JS/TS and Python
- Dependency on multiple package managers (pnpm + pip)

## Related Decisions

- [ADR-0001: Use Monorepo Structure](0001-use-monorepo.md)
- [ADR-0003: Database Design](0003-database-design.md)
