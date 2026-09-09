# ADR-0009: Container Strategy

## Status

**Accepted** | 2024-01-XX

## Context

We need a containerization strategy that:
- Provides consistent development environments
- Enables easy deployment
- Supports local development with hot-reload
- Is production-ready for future phases

## Decision

### Docker Compose for Development

#### Services (Phase 0)
| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| web | Node.js 20 Alpine | 3000 | Next.js frontend |
| api | Python 3.11 Slim | 8000 | FastAPI backend |
| worker | Python 3.11 Slim | - | Background jobs |
| db | PostgreSQL 16 Alpine | 5432 | Primary database |
| redis | Redis 7 Alpine | 6379 | Cache/broker |

### Multi-stage Builds for Production

#### Web Dockerfile Stages:
1. **deps**: Install npm dependencies (cached layer)
2. **builder**: Build Next.js application
3. **runner**: Minimal production image

#### API Dockerfile Stages:
1. **deps**: Create venv, install Python packages
2. **production**: Copy code + venv, run with uvicorn

### Volume Strategy
| Path | Purpose |
|------|---------|
| `./apps/web:/app` | Hot-reload during development |
| `postgres_data` | Persistent database storage |
| `redis_data` | Persistent cache storage |

## Alternatives Considered

### Option A: Podman/Buildah
- Daemonless, rootless containers
- Less ecosystem support
- Rejected for broader compatibility

### Option B: Docker + Docker Compose (CHOSEN)
- Industry standard
- Excellent tooling support
- Large community knowledge base
- Works well with CI/CD platforms

## Consequences

### Positive
- Reproducible environments
- Easy onboarding ("just run docker compose up")
- Consistent dev/staging/prod
- Good caching with multi-stage builds

### Negative
- Docker Desktop resource usage on Mac/Windows
- Need to manage image sizes
- Learning curve for team members new to Docker

## Implementation Status
- ✅ Phase 0: Full docker-compose setup, all services defined
- 🟡 Phase 1+: Production optimizations, security scanning

## Related Decisions

- [ADR-0001: Use Monorepo Structure](0001-use-monorepo.md)
- [ADR-0002: Technology Stack Selection](0002-technology-stack.md)
