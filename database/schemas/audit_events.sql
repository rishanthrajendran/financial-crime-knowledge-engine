-- =============================================================================
-- Financial Crime Knowledge Engine
-- audit_events table schema
-- =============================================================================

CREATE TABLE IF NOT EXISTS audit_events (
    -- Primary key (UUID v4)
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Action information
    action VARCHAR(128) NOT NULL,  -- e.g., "document.create", "user.login"
    
    -- Actor information
    actor VARCHAR(256),  -- User ID or system identifier
    actor_type VARCHAR(64),  -- 'user', 'system', 'api_key', 'worker'
    
    -- Target resource
    resource_type VARCHAR(128),  -- e.g., "knowledge_document", "user"
    resource_id UUID,
    
    -- Additional details
    details_json JSONB,  -- Flexible storage for action-specific data
    
    -- Request context
    ip_address VARCHAR(45),  -- IPv4 or IPv6
    user_agent VARCHAR(512),
    
    -- Timestamp
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for audit queries
CREATE INDEX IF NOT EXISTS ix_audit_events_action 
    ON audit_events(action);
    
CREATE INDEX IF NOT EXISTS ix_audit_events_timestamp 
    ON audit_events(timestamp DESC);
    
CREATE INDEX IF NOT EXISTS ix_audit_events_actor 
    ON audit_events(actor) 
    WHERE actor IS NOT NULL;

CREATE INDEX IF NOT EXISTS ix_audit_events_resource 
    ON audit_events(resource_type, resource_id)
    WHERE resource_id IS NOT NULL;

-- Composite index for common audit queries
CREATE INDEX IF NOT EXISTS ix_audit_events_action_timestamp 
    ON audit_events(action, timestamp DESC);
