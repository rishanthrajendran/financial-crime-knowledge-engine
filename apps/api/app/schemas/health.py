"""
Health check and system status schemas.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: Literal["healthy", "unhealthy"] = Field(
        description="Overall health status"
    )
    version: str = Field(description="Application version")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp in UTC",
    )


class ReadinessCheck(BaseModel):
    """Individual readiness check result."""

    name: str = Field(description="Check name")
    status: Literal["ok", "error"] = Field(description="Check status")
    message: str | None = Field(default=None, description="Optional error message")


class ReadinessResponse(BaseModel):
    """Readiness probe response."""

    status: Literal["ready", "not_ready"] = Field(
        description="Overall readiness status"
    )
    checks: list[ReadinessCheck] = Field(description="Individual checks")


class VersionInfo(BaseModel):
    """Version information response."""

    version: str = Field(description="Software version")
    phase: str = Field(description="Current development phase")
    api_version: str = Field(description="API version")
    knowledge_base_version: str = Field(description="Knowledge Base dependency version")


class VersionResponse(BaseModel):
    """Version endpoint response."""

    data: VersionInfo
