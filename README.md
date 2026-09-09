# Financial Crime Knowledge Engine

> **Phase 0 - Software Foundation** | Version 0.1.0

A comprehensive knowledge engine for financial crime prevention, AML compliance, and regulatory intelligence.

## ⚠️ Current Status: Phase 0 - Software Foundation

This repository represents **Phase 0** of the Financial Crime Knowledge Engine. At this stage, we have established:

### ✅ IMPLEMENTED (Working)

| Component | Status | Description |
|-----------|--------|-------------|
| Monorepo Structure | ✅ Complete | pnpm workspaces with apps/* and packages/* |
| Next.js Frontend Shell | ✅ Complete | Landing page with system status display |
| FastAPI Backend Foundation | ✅ Complete | Health checks, config, database setup |
| Worker Framework | ✅ Scaffolded | Job execution model and registry |
| Database Schema | ✅ Complete | Alembic migrations for core tables |
| Docker Configuration | ✅ Complete | docker-compose with all services |
| CI/CD Pipeline | ✅ Complete | Lint, type-check, test, security jobs |
| Documentation | ✅ Complete | Architecture, ADRs, security docs |
| Validation Script | ✅ Complete | Phase 0 verification script |

### 📋 PLANNED (Future Phases)

| Feature | Target Phase | Description |
|---------|--------------|-------------|
| Authentication & RBAC | Phase 1 | User management, role-based access |
| Knowledge Ingestion Pipeline | Phase 1 | Import from Knowledge Base repository |
| Vector Search / RAG | Phase 2 | AI-powered semantic search |
| Graph Search | Phase 2 | Relationship-based knowledge queries |
| Assessment Engine | Phase 3 | Automated risk assessment workflows |
| Real-time Monitoring | Phase 3 | Dashboard and alerting |

## Quick Start

### Prerequisites

- Node.js >= 18.0.0
- pnpm >= 8.0.0
- Python >= 3.11
- Docker & Docker Compose
- uv (Python package manager) or pip

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd financial-crime-knowledge-engine

# Install dependencies
pnpm install

# Start all services with Docker Compose
docker compose up -d

# Start development servers
pnpm dev:web    # Next.js on :3000
```

### Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| web | 3000 | Next.js frontend |
| api | 8000 | FastAPI backend |
| worker | - | Background job processor |
| db | 5432 | PostgreSQL 16 |
| redis | 6379 | Redis 7 |

## Project Structure

```
financial-crime-knowledge-engine/
├── apps/
│   ├── web/          # Next.js 16 frontend
│   ├── api/          # FastAPI Python backend
│   └── worker/       # Python worker foundation
├── packages/
│   ├── ui/           # Shared UI components
│   ├── knowledge/    # Knowledge domain types
│   ├── sdk/          # API client SDK
│   └── shared/       # Shared utilities
├── database/         # Migrations, seeds, schemas
├── knowledge/        # Integration specs and manifests
├── infrastructure/   # Docker, K8s, Terraform configs
├── scripts/          # Utility scripts
├── tests/            # Test suites
└── docs/             # Documentation
```

## API Endpoints (Phase 0)

| Endpoint | Method | Status | Description |
|----------|--------|--------|-------------|
| `/health` | GET | ✅ | Health check |
| `/ready` | GET | ✅ | Readiness probe |
| `/version` | GET | ✅ | Version information |

## Documentation

- [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Architecture Decision Records](docs/adr/)
- [Security Baseline](docs/security/SECURITY_BASELINE.md)
- [Development Standards](docs/development/ENGINEERING_STANDARDS.md)
- [Implementation Status](docs/development/IMPLEMENTATION_STATUS.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

## Version Information

- **Software Version**: 0.1.0 (Phase 0 baseline)
- **Knowledge Base Dependency**: v3.0.1 LTS (external specification)

---

> **Note**: This is a new software implementation repository. It is separate from the Knowledge Base (specification) repository.
