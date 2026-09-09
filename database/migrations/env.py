"""
Alembic environment configuration for FCKE database migrations.

This file configures the migration environment and provides
the online/offline migration functions.
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

# Import models for autogenerate detection
from app.models.base import Base
# Import all models to ensure they're registered with Base.metadata
# from app.models.knowledge_document import KnowledgeDocument  # Phase 1+
# from app.models.knowledge_source import KnowledgeSource  # Phase 1+
# from app.models.audit_event import AuditEvent  # Phase 1+

# Alembic Config object
config = context.config

# Python logging setup from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This creates a SQL script that can be applied to a database
    without requiring a live database connection.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # Compare types for autogenerate
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Run migrations with an existing connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # Compare types for autogenerate
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Run migrations in 'online' mode with async engine.
    
    This connects to a live database and applies migrations.
    """
    # Get the configuration section and merge -x arguments into it
    # The CI passes: alembic -c ../../alembic.ini -x sqlalchemy.url=$DATABASE_URL
    # These -x args are stored in config.x_args, NOT in the ini section
    # We must merge them so async_engine_from_config() can find sqlalchemy.url
    section = config.get_section(config.config_ini_section, {})
    
    # Extract sqlalchemy.* options from -x arguments and merge into section
    for key, value in config.x_args.items():
        if key.startswith("sqlalchemy."):
            section[key] = value
    
    connectable = async_engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
