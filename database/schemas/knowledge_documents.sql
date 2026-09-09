-- =============================================================================
-- Financial Crime Knowledge Engine
-- knowledge_documents table schema
-- =============================================================================

-- This file contains the SQL DDL for the knowledge_documents table.
-- For actual migrations, use Alembic.

CREATE TABLE IF NOT EXISTS knowledge_documents (
    -- Primary key (UUID v4)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Foreign key to knowledge_sources
    source_id UUID NOT NULL REFERENCES knowledge_sources(id),
    
    -- Version tracking
    version VARCHAR(64) NOT NULL,
    phase VARCHAR(32) NOT NULL DEFAULT 'phase0',
    
    -- Content integrity
    checksum VARCHAR(128),  -- SHA-256 hash of document content
    
    -- Document metadata
    status VARCHAR(32) NOT NULL DEFAULT 'pending',  -- pending, processing, active, error
    document_type VARCHAR(64),  -- regulation, guidance, case_study, definition, etc.
    title VARCHAR(512),
    content_path VARCHAR(1024),  -- Path to content in storage
    
    -- Flexible metadata (JSON)
    metadata_json JSONB,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    -- Soft delete
    deleted_at TIMESTAMPTZ
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_source_id 
    ON knowledge_documents(source_id);
    
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_status 
    ON knowledge_documents(status);
    
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_document_type 
    ON knowledge_documents(document_type);

CREATE INDEX IF NOT EXISTS ix_knowledge_documents_created_at 
    ON knowledge_documents(created_at DESC);

-- Partial index for active (non-deleted) documents
CREATE INDEX IF NOT EXISTS ix_knowledge_documents_active 
    ON knowledge_documents(source_id, status) 
    WHERE deleted_at IS NULL;
