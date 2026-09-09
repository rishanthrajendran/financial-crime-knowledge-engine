# System Architecture

> **Status**: Phase 0 - Software Foundation  
> **Last Updated**: 2024-01-XX  
> **Version**: 0.1.0

## Overview

The Financial Crime Knowledge Engine (FCKE) is a comprehensive platform for managing, searching, and reasoning about financial crime knowledge. This document describes the system architecture at its current state (Phase 0) and planned future states.

### Current State: Phase 0 - Foundation

At Phase 0, we have established:

| Component | Status | Description |
|-----------|--------|-------------|
| Monorepo Structure | ✅ IMPLEMENTED | pnpm workspaces with apps/* and packages/* |
| Next.js Frontend Shell | ✅ IMPLEMENTED | Landing page with system status display |
| FastAPI Backend Foundation | ✅ IMPLEMENTED | Health checks, config, database setup |
| Worker Framework | ✅ SCAFFOLDED | Job execution model and registry |
| Database Schema | ✅ SCAFFOLDED | Alembic migrations defined |
| Docker Configuration | ✅ IMPLEMENTED | docker-compose with all services |
| CI/CD Pipeline | ✅ IMPLEMENTED | GitHub Actions workflow |

---

## System Context Diagram

```mermaid
graph TB
    subgraph "Users"
        U[Compliance Analyst]
        A[Administrator]
    end

    subgraph "FCKE Platform - Phase 0"
        subgraph "Frontend Layer"
            WEB[Next.js App<br/>:3000]
        end

        subgraph "API Layer"
            API[FastAPI Server<br/>:8000]
        end

        subgraph "Processing Layer"
            WORKER[Background Worker]
        end

        subgraph "Data Layer"
            DB[(PostgreSQL 16)]
            REDIS[(Redis 7)]
        end
    end

    subgraph "External - Planned"
        KB[Knowledge Base Repo<br/>v3.0.1 LTS]
        AI[AI Services<br/>Phase 2+]
    end

    U --> WEB
    A --> WEB
    WEB --> API
    API --> DB
    API --> REDIS
    WORKER --> DB
    WORKER --> REDIS
    
    KB -.->|Phase 1+| WORKER
    AI -.->|Phase 2+| API
```

---

## Component Architecture

```mermaid
graph LR
    subgraph "apps/web - Next.js Frontend"
        W1[src/app/page.tsx<br/>Landing Page]
        W2[src/app/api/health<br/>Health Proxy]
        W3[src/lib/api-client.ts<br/>API Client]
    end

    subgraph "apps/api - FastAPI Backend"
        A1[app/main.py<br/>Application Entry]
        A2[app/config.py<br/>Configuration]
        A3[app/database.py<br/>DB Session Mgmt]
        A4[app/models/<br/>SQLAlchemy Models]
        A5[app/schemas/<br/>Pydantic Schemas]
        A6[app/core/<br/>Logging & Errors]
        A7[app/api/v1/<br/>API Router]
    end

    subgraph "apps/worker - Background Jobs"
        W1[job_base.py<br/>Abstract Job Class]
        W2[registry.py<br/>Job Registry]
        W3[executor.py<br/>Job Executor]
    end

    subgraph "packages - Shared Code"
        P1[@fcke/ui<br/>UI Components]
        P2[@fcke/knowledge<br/>Domain Types]
        P3[@fcke/sdk<br/>API Client SDK]
        P4[@fcke/shared<br/>Utilities]
    end
```

---

## Data Flow Diagram

### Phase 0 Data Flow (Current)

```mermaid
sequenceDiagram
    participant User as Browser
    participant Web as Next.js :3000
    participant API as FastAPI :8000
    participant DB as PostgreSQL

    User->>Web: GET /
    Web-->>User: Landing Page HTML

    User->>Web: GET /api/health
    Web->>API: GET /health (proxy)
    API-->>Web: {status: healthy}
    Web-->>User: Aggregated health status

    User->>API: GET /ready
    API->>DB: SELECT 1 (check)
    DB-->>API: OK
    API-->>User: {status: ready}
```

### Phase 1+ Data Flow (Planned)

```mermaid
sequenceDiagram
    participant User as Browser
    participant Web as Next.js
    participant API as FastAPI
    participant Worker as Job Worker
    participant DB as PostgreSQL
    participant KB as Knowledge Base

    Note over Worker: Scheduled ingestion job
    Worker->>KB: Clone/pull repository
    KB-->>Worker: Repository content
    Worker->>DB: INSERT documents
    Worker->>Worker: Generate embeddings (Phase 2)
    
    User->>Web: Search query
    Web->>API: POST /v1/knowledge/search
    API->>DB: Query documents
    DB-->>API: Results
    API-->>Web: Search results
    Web-->>User: Display results
```

---

## Trust Boundaries

```mermaid
graph TB
    subgraph "Public Internet"
        USER[End Users]
    end

    subgraph "DMZ / Edge"
        CDN[CDN - Future]
        LB[Load Balancer - Future]
    end

    subgraph "Application Tier - TRUST BOUNDARY 1"
        WEB[Next.js Frontend]
        API[FastAPI Backend]
    end

    subgraph "Processing Tier - TRUST BOUNDARY 2"
        WORKER[Background Worker]
    end

    subgraph "Data Tier - TRUST BOUNDARY 3"
        DB[(PostgreSQL)]
        REDIS[(Redis)]
    end

    USER -->|HTTPS| WEB
    USER -.->|Future| CDN
    CDN -.->|Future| LB
    LB -.->|Internal| WEB
    WEB -->|Internal API| API
    API -->|Async Tasks| WORKER
    API -->|Encrypted| DB
    API -->|Encrypted| REDIS
    WORKER -->|Encrypted| DB
```

**Trust Boundary Notes (Phase 0):**
- All internal communication is currently on Docker network
- TLS termination not yet implemented (planned for Phase 1)
- No authentication layer yet (planned for Phase 1)

---

## Technology Decisions

### Implemented Technologies

| Technology | Version | Purpose | Decision Date |
|------------|---------|---------|---------------|
| Next.js | 15+ | Frontend framework | 2024-01 |
| React | 19+ | UI library | 2024-01 |
| TypeScript | 5+ | Type safety | 2024-01 |
| Tailwind CSS | 4+ | Styling | 2024-01 |
| FastAPI | 0.115+ | API framework | 2024-01 |
| Python | 3.11+ | Backend runtime | 2024-01 |
| SQLAlchemy | 2.0+ | ORM | 2024-01 |
| Pydantic | v2 | Validation | 2024-01 |
| Alembic | - | Migrations | 2024-01 |
| PostgreSQL | 16 | Primary database | 2024-01 |
| Redis | 7 | Cache/broker | 2024-01 |
| Docker | - | Containerization | 2024-01 |
| pnpm | 9+ | JS package manager | 2024-01 |

### Planned Technologies (Future Phases)

| Technology | Target Phase | Purpose |
|------------|--------------|---------|
| OpenAI/LLM APIs | Phase 2 | Embeddings and RAG |
| pgvector | Phase 2 | Vector search |
| Redis Stack | Phase 2 | Vector storage |
| Keycloak/Auth0 | Phase 1 | Authentication |
| Prometheus/Grafana | Phase 2 | Observability |
| Kubernetes | Phase 3 | Orchestration |

---

## Deployment Architecture (Planned)

```mermaid
graph TB
    subgraph "Production - Phase 3+"
        subgraph "Kubernetes Cluster"
            subgraph "Web Tier"
                WEB_PODS[Web Pods x3]
            end
            subgraph "API Tier"
                API_PODS[API Pods x3]
            end
            subgraph "Worker Tier"
                WORKER_PODS[Worker Pods x2]
            end
            subgraph "Data Tier"
                PG_CLUSTER[PostgreSQL HA]
                REDIS_CLUSTER[Redis Cluster]
            end
        end
        
        subgraph "External"
            CDNs[CDN]
            MONITORING[Monitoring Stack]
        end
    end
```

---

## Status Legend

| Status | Meaning |
|--------|---------|
| ✅ **IMPLEMENTED** | Working code exists and is tested |
| 🟡 **SCAFFOLDED** | Structure exists, minimal logic |
| 🔵 **PLANNED** | Design complete, implementation pending |
| ⚪ **SPECIFICATION_ONLY** | Documentation only |

---

## Related Documents

- [Architecture Decision Records](../adr/)
- [Domain Model](DOMAIN_MODEL.md)
- [Knowledge Base Integration](KNOWLEDGE_BASE_INTEGRATION.md)
- [AI/RAG Architecture](AI_RAG_ARCHITECTURE.md)
- [Search Architecture](SEARCH_ARCHITECTURE.md)
