"""
Async SQLAlchemy database session management.

Provides async engine, session factory, and dependency injection
for FastAPI endpoints.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings


# Create async engine
engine = create_async_engine(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides an async database session.
    
    Usage in FastAPI:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> bool:
    """
    Check if database connection is healthy.
    
    Returns True if connection succeeds, False otherwise.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
            return True
    except Exception:
        return False


async def dispose_engine() -> None:
    """Dispose of the database engine (for shutdown)."""
    await engine.dispose()
