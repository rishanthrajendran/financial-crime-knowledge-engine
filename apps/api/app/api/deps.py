"""
Dependency injection for FastAPI endpoints.

Provides reusable dependencies for database sessions,
current user (future), and other common dependencies.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_async_session, check_database_connection
from app.core.errors import FCKEError


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async for session in get_async_session():
        yield session


async def get_redis_health() -> bool:
    """
    Check Redis health.
    
    Phase 0: Returns True as placeholder.
    Phase 1+: Will implement actual Redis health check.
    """
    # TODO: Implement actual Redis health check in Phase 1
    return True


async def verify_readiness() -> dict[str, bool]:
    """
    Verify all dependencies are ready.
    
    Returns a dict of component names to their ready status.
    """
    db_healthy = await check_database_connection()
    redis_healthy = await get_redis_health()
    
    return {
        "database": db_healthy,
        "redis": redis_healthy,
    }
