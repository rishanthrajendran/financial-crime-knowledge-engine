# Changelog

All notable changes to the Financial Crime Knowledge Engine will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX (Phase 0 Baseline)

### Added

#### Monorepo Foundation
- Initial monorepo structure with pnpm workspaces
- Root configuration: package.json, pnpm-workspace.yaml, tsconfig.base.json
- Comprehensive .gitignore for Node.js, Python, Docker, IDE files
- .editorconfig for consistent coding style
- .env.example with all required environment variables

#### Frontend (apps/web)
- Next.js 16 application shell with App Router
- TypeScript 5 strict mode configuration
- Tailwind CSS 4 integration
- Root layout with metadata and providers
- Landing page displaying system status and version info
- Health check API proxy endpoint
- Typed API client abstraction

#### Backend (apps/api)
- FastAPI application foundation
- Pydantic v2 settings configuration
- Async SQLAlchemy session management
- Base model with UUID, timestamps, soft delete mixins
- Pydantic response schemas
- Dependency injection framework
- API v1 router structure
- Structured logging setup
- Exception handling framework
- Health, readiness, and version endpoints

#### Worker (apps/worker)
- Abstract job base class with execution model
- Job registry pattern
- Job executor implementation
- Job type definitions: knowledge_ingestion, embedding_generation, indexing, assessment_processing

#### Database
- Alembic migration configuration
- Core schema definitions:
  - `knowledge_documents` table
  - `knowledge_sources` table
  - `audit_events` table
- SQL schema reference files

#### Infrastructure
- Docker Compose configuration for all services
- Multi-stage Dockerfile for Next.js web app
- Dockerfile for FastAPI API service
- Dockerfile for Python worker service
- .dockerignore files

#### CI/CD
- GitHub Actions workflow with:
  - Lint job (ESLint + Ruff)
  - Type-check job (TypeScript + mypy)
  - Test jobs (pytest + vitest)
  - Security audit job
  - Build verification job

#### Documentation
- System Architecture document with Mermaid diagrams
- Architecture Decision Records (ADRs) 0001-0010:
  - 0001: Use Monorepo Structure
  - 0002: Technology Stack Selection
  - 0003: Database Design
  - 0004: API Design Standards
  - 0005: Authentication Strategy
  - 0006: Error Handling Approach
  - 0007: Logging Strategy
  - 0008: Testing Strategy
  - 0009: Container Strategy
  - 0010: Observability Strategy
- Knowledge Base Integration specification
- Source of Truth document
- Domain Model documentation
- AI/RAG Architecture (specification only)
- Search Architecture design
- Security Baseline
- Authentication & Authorization design
- Observability guide
- Testing Strategy
- Engineering Standards
- Implementation Status (honest assessment)
- Traceability Matrix
- Contributing guidelines

#### Testing
- Backend health endpoint tests
- Frontend smoke tests
- Integration database tests
- Test fixtures structure

#### Tooling
- Phase 0 validation script (`scripts/validate_phase0.py`)

### Status Notes

This release establishes the **software foundation** only. No business logic,
knowledge processing, or AI features are implemented. Those are planned for
future phases.

---

## [Unreleased]

### Planned for Phase 1
- User authentication and authorization
- Knowledge ingestion pipeline from Knowledge Base repository
- Basic CRUD operations for knowledge documents
- Admin interface for content management

### Planned for Phase 2
- Vector embeddings generation
- Semantic search (RAG)
- Graph-based relationship queries
- Assessment workflow engine

### Planned for Phase 3
- Real-time monitoring dashboard
- Advanced analytics
- Multi-tenant support
- Production hardening
