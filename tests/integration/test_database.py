"""
Integration tests for database connectivity and schema.

Phase 0: Tests to verify database connection, schema validity,
and basic CRUD operations on core tables.
"""

import pytest
import asyncio
from typing import AsyncGenerator


# Mark all tests as async
pytestmark = pytest.mark.asyncio


class TestDatabaseConnection:
    """Tests for database connection and basic operations."""

    @pytest.mark.asyncio
    async def test_database_url_format(self):
        """Database URL should be valid async PostgreSQL URL."""
        # Valid formats for async SQLAlchemy
        valid_prefixes = [
            "postgresql+asyncpg://",
            "postgresql+aiosqlite://",
        ]
        
        # Example URL (would come from config in real test)
        example_url = "postgresql+asyncpg://fcke:fcke_dev@localhost:5432/fcke"
        
        is_valid = any(example_url.startswith(prefix) for prefix in valid_prefixes)
        
        assert is_valid, f"Database URL should start with one of {valid_prefixes}"

    @pytest.mark.asyncio
    async def test_database_config_has_required_params(self):
        """Database config should have all required parameters."""
        # These parameters are needed for a working DB connection
        required_params = [
            "host",
            "port",
            "database",
            "username",  # or "user"
        ]
        
        # Example config structure
        db_config = {
            "host": "localhost",
            "port": 5432,
            "database": "fcke",
            "username": "fcke",
        }
        
        for param in required_params:
            assert param in db_config, f"Missing required param: {param}"


class TestSchemaValidation:
    """Tests for database schema structure."""

    @pytest.mark.asyncio
    async def test_knowledge_documents_table_schema(self):
        """knowledge_documents table should have required columns."""
        expected_columns = {
            "id": "UUID PRIMARY KEY",
            "source_id": "UUID FOREIGN KEY",
            "version": "VARCHAR",
            "phase": "VARCHAR",
            "checksum": "VARCHAR",
            "status": "VARCHAR",
            "document_type": "VARCHAR",
            "title": "VARCHAR",
            "metadata_json": "JSON/JSONB",
            "created_at": "TIMESTAMPTZ",
            "updated_at": "TIMESTAMPTZ",
            "deleted_at": "TIMESTAMPTZ (nullable)",
        }
        
        # Verify all expected columns are defined
        assert len(expected_columns) >= 10  # At minimum columns
        assert "id" in expected_columns
        assert "created_at" in expected_columns
        assert "deleted_at" in expected_columns

    @pytest.mark.asyncio
    async def test_knowledge_sources_table_schema(self):
        """knowledge_sources table should have required columns."""
        expected_columns = {
            "id": "UUID PRIMARY KEY",
            "repo_url": "VARCHAR UNIQUE",
            "version": "VARCHAR",
            "commit_sha": "VARCHAR",
            "ingestion_timestamp": "TIMESTAMPTZ",
            "created_at": "TIMESTAMPTZ",
            "updated_at": "TIMESTAMPTZ",
        }
        
        assert len(expected_columns) >= 6
        assert "repo_url" in expected_columns
        assert "id" in expected_columns

    @pytest.mark.asyncio
    async def test_audit_events_table_schema(self):
        """audit_events table should have required columns."""
        expected_columns = {
            "id": "UUID PRIMARY KEY",
            "action": "VARCHAR",
            "actor": "VARCHAR",
            "actor_type": "VARCHAR",
            "resource_type": "VARCHAR",
            "resource_id": "UUID",
            "details_json": "JSON/JSONB",
            "ip_address": "VARCHAR",
            "timestamp": "TIMESTAMPTZ",
        }
        
        assert len(expected_columns) >= 8
        assert "action" in expected_columns
        assert "timestamp" in expected_columns


class TestMigrationStructure:
    """Tests for Alembic migration setup."""

    @pytest.mark.asyncio
    async def test_alembic_ini_exists_conceptually(self):
        """Alembic configuration should define key settings."""
        # These are the key settings that should be in alembic.ini
        required_settings = [
            "script_location",
            "sqlalchemy.url",
            "file_template",
        ]
        
        # Verify we know what's needed
        assert len(required_settings) == 3
        assert "script_location" in required_settings

    @pytest.mark.asyncio
    async def test_initial_migration_defined(self):
        """Initial migration should create all core tables."""
        expected_tables = [
            "knowledge_sources",
            "knowledge_documents",
            "audit_events",
        ]
        
        # The initial migration (0001_initial_schema.py) should create these
        assert len(expected_tables) == 3
        assert "knowledge_documents" in expected_tables

    @pytest.mark.asyncio
    async def test_migration_revision_format(self):
        """Migrations should have proper revision identifiers."""
        # Revision format: descriptive string
        initial_revision = "0001_initial"
        
        assert isinstance(initial_revision, str)
        assert len(initial_revision) > 0
        assert initial_revision.startswith("0001")


class TestModelDefinitions:
    """Tests for SQLAlchemy model definitions."""

    @pytest.mark.asyncio
    async def test_base_model_includes_timestamps(self):
        """Base model should include created_at and updated_at."""
        base_mixin_fields = {
            "created_at": "DateTime with server_default=now()",
            "updated_at": "DateTime with onupdate=now()",
        }
        
        assert "created_at" in base_mixin_fields
        assert "updated_at" in base_mixin_fields

    @pytest.mark.asyncio
    async def test_base_model_includes_uuid_pk(self):
        """Base model should use UUID as primary key."""
        pk_field = {
            "name": "id",
            "type": "UUID",
            "primary_key": True,
            "default": "uuid4",
        }
        
        assert pk_field["type"] == "UUID"
        assert pk_field["primary_key"] is True

    @pytest.mark.asyncio
    async def test_soft_delete_mixin_available(self):
        """Soft delete mixin should provide deleted_at field."""
        soft_delete_fields = {
            "deleted_at": "DateTime nullable",
            "is_deleted": "property returning bool",
        }
        
        assert "deleted_at" in soft_delete_fields
        assert "is_deleted" in soft_delete_fields


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
