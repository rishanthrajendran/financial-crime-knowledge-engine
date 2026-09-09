-- =============================================================================
-- Financial Crime Knowledge Engine
-- knowledge_sources table schema
-- =============================================================================

CREATE TABLE IF NOT EXISTS knowledge_sources (
    -- Primary key (UUID v4)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Source identification
    repo_url VARCHAR(512) NOT NULL UNIQUE,  -- Git repository URL
    
    -- Version tracking
    version VARCHAR(64),  -- e.g., "v3.0.1"
    commit_sha VARCHAR(64),  -- Full SHA of last ingested commit
    
    -- Ingestion metadata
    ingestion_timestamp TIMESTAMPTZ,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS ix_knowledge_sources_repo_url 
    ON knowledge_sources(repo_url);
