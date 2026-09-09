"""
Initial schema for Financial Crime Knowledge Engine - Phase 0

This migration creates the core tables:
- knowledge_documents: Stores ingested knowledge documents
- knowledge_sources: Tracks source repositories
- audit_events: Audit log for compliance

Revision ID: 0001_initial
Revises: None
Create Date: 2024-01-01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers
revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create initial schema tables."""
    
    # =========================================================================
    # knowledge_sources table
    # =========================================================================
    op.create_table(
        "knowledge_sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("repo_url", sa.String(512), nullable=False, unique=True),
        sa.Column("version", sa.String(64), nullable=True),
        sa.Column("commit_sha", sa.String(64), nullable=True),
        sa.Column("ingestion_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "ix_knowledge_sources_repo_url",
        "knowledge_sources",
        ["repo_url"],
    )
    
    # =========================================================================
    # knowledge_documents table
    # =========================================================================
    op.create_table(
        "knowledge_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", sa.String(64), nullable=False),
        sa.Column("phase", sa.String(32), nullable=False, default="phase0"),
        sa.Column("checksum", sa.String(128), nullable=True),
        sa.Column("status", sa.String(32), nullable=False, default="pending"),
        sa.Column("document_type", sa.String(64), nullable=True),
        sa.Column("title", sa.String(512), nullable=True),
        sa.Column("content_path", sa.String(1024), nullable=True),
        sa.Column("metadata_json", sa.JSON, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["source_id"], ["knowledge_sources.id"]),
    )
    op.create_index(
        "ix_knowledge_documents_source_id",
        "knowledge_documents",
        ["source_id"],
    )
    op.create_index(
        "ix_knowledge_documents_status",
        "knowledge_documents",
        ["status"],
    )
    op.create_index(
        "ix_knowledge_documents_document_type",
        "knowledge_documents",
        ["document_type"],
    )
    
    # =========================================================================
    # audit_events table
    # =========================================================================
    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("actor", sa.String(256), nullable=True),
        sa.Column("actor_type", sa.String(64), nullable=True),
        sa.Column("resource_type", sa.String(128), nullable=True),
        sa.Column("resource_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("details_json", sa.JSON, nullable=True),
        sa.Column("ip_address", sa.String(45), nullable=True),
        sa.Column("user_agent", sa.String(512), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "ix_audit_events_action",
        "audit_events",
        ["action"],
    )
    op.create_index(
        "ix_audit_events_timestamp",
        "audit_events",
        ["timestamp"],
    )
    op.create_index(
        "ix_audit_events_resource",
        "audit_events",
        ["resource_type", "resource_id"],
    )


def downgrade() -> None:
    """Drop all initial schema tables."""
    op.drop_table("audit_events")
    op.drop_table("knowledge_documents")
    op.drop_table("knowledge_sources")
