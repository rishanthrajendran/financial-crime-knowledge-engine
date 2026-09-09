"""
Base SQLAlchemy model with common mixins.

Provides:
- UUIDMixin: Primary key as UUID
- TimestampMixin: created_at and updated_at timestamps
- SoftDeleteMixin: Soft delete with deleted_at timestamp
- Base: Combined base class for all models
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class UUIDMixin:
    """Mixin that adds a UUID primary key."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete capability with deleted_at timestamp."""

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


class Base(DeclarativeBase, UUIDMixin, TimestampMixin):
    """
    Base class for all SQLAlchemy models.

    Combines UUID primary key and automatic timestamps.
    Add SoftDeleteMixin to models that need soft delete.

    Example:
        class KnowledgeDocument(Base, SoftDeleteMixin):
            __tablename__ = "knowledge_documents"
            ...
    """

    pass
