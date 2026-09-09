# ADR-0003: Database Design

## Status

**Accepted** | 2024-01-XX

## Context

We need to design a database schema that supports:
- Knowledge document storage and versioning
- Source repository tracking
- Audit logging for compliance
- Future extensibility for AI features (embeddings, vectors)

## Decision

### Core Tables (Phase 0)

#### knowledge_sources
Tracks external knowledge source repositories.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| repo_url | VARCHAR(512) UNIQUE | Git repository URL |
| version | VARCHAR(64) | Version tag/branch |
| commit_sha | VARCHAR(64) | Last ingested commit |
| ingestion_timestamp | TIMESTAMPTZ | Last successful ingestion |

#### knowledge_documents
Stores individual knowledge documents with soft delete support.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| source_id | UUID FK | Reference to knowledge_source |
| version | VARCHAR(64) | Document version |
| phase | VARCHAR(32) | Development phase origin |
| checksum | VARCHAR(128) | Content hash for integrity |
| status | VARCHAR(32) | Processing status |
| document_type | VARCHAR(64) | Classification type |
| metadata_json | JSONB | Flexible metadata storage |
| deleted_at | TIMESTAMPTZ | Soft delete timestamp |

#### audit_events
Immutable audit log for compliance and debugging.

| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| action | VARCHAR(128) | Action performed |
| actor | VARCHAR(256) | Who performed action |
| resource_type | VARCHAR(128) | Target type |
| resource_id | UUID | Target ID |
| details_json | JSONB | Action details |
| timestamp | TIMESTAMPTZ | When action occurred |

### Design Patterns
1. **UUID Primary Keys**: Distributed-friendly, no sequence conflicts
2. **Soft Delete**: Preserve data for audit, allow recovery
3. **JSONB Columns**: Flexible schema evolution
4. **Timestamped**: All tables have created_at/updated_at

## Alternatives Considered

### Option A: Single Table per Entity Type (CHOSEN)
- Clear separation, easy to understand
- Good query performance with proper indexes
- Standard relational approach

### Option B: Polymorphic Document Table
- More flexible but complex queries
- Harder to maintain data integrity
- Rejected for initial implementation

## Consequences

### Positive
- Clear, maintainable schema
- Good performance characteristics
- Supports compliance requirements
- Extensible for future needs

### Negative
- May need denormalization for search performance (Phase 2)
- Vector columns will require pgvector extension (Phase 2)

## Future Considerations (Planned)
- Phase 2: Add embedding columns to knowledge_documents
- Phase 2: Create vector index table
- Phase 3: Consider time-series partitioning for audit_events

## Related Decisions

- [ADR-0002: Technology Stack Selection](0002-technology-stack.md)
- [ADR-0006: Error Handling Approach](0006-error-handling.md)
