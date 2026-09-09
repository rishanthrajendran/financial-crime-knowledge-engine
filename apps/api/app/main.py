"""
Financial Crime Knowledge Engine - FastAPI Application

Main entry point for the API server. Provides:
- Health check endpoints
- Readiness probe
- Version information
- API v1 router (placeholder for Phase 1+)
"""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.deps import verify_readiness
from app.api.v1.router import router as v1_router
from app.config import settings
from app.core.errors import FCKEError
from app.core.logging import get_logger, setup_logging

# Setup structured logging
setup_logging(
    log_level="DEBUG" if settings.debug else "INFO",
    json_logs=settings.is_production,
)

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info(
        "starting_application",
        version=settings.app_version,
        environment=settings.app_env,
    )

    yield

    # Shutdown
    logger.info("shutting_down_application")

    # Cleanup database connections
    from app.database import dispose_engine
    await dispose_engine()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=(
        "Financial Crime Knowledge Engine API\n\n"
        "## Phase 0 - Software Foundation\n\n"
        "This is the initial foundation release. "
        "Business endpoints will be added in future phases.\n\n"
        "**Current Status:** Health checks and system endpoints only."
    ),
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(FCKEError)
async def fcke_error_handler(request: Request, exc: FCKEError) -> JSONResponse:
    """Handle custom FCKE exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.to_dict()},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions."""
    logger.exception("unhandled_exception", path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            }
        },
    )


# Include routers
app.include_router(v1_router)


# =============================================================================
# System Endpoints (Phase 0)
# =============================================================================


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns basic health status without checking dependencies.
    Use / readiness for dependency checks.
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/ready", tags=["system"])
async def readiness_check() -> dict[str, object]:
    """
    Readiness probe endpoint.

    Checks all dependencies (database, redis) and returns
    their individual statuses.
    """
    checks = await verify_readiness()

    all_healthy = all(checks.values())
    status: Literal["ready", "not_ready"] = "ready" if all_healthy else "not_ready"

    return {
        "status": status,
        "checks": [
            {
                "name": name,
                "status": "ok" if healthy else "error",
                "message": None if healthy else f"{name} is not available",
            }
            for name, healthy in checks.items()
        ],
    }


@app.get("/version", tags=["system"])
async def version_info() -> dict[str, str]:
    """
    Version information endpoint.

    Returns current software version and dependency versions.
    """
    return {
        "data": {
            "version": settings.app_version,
            "phase": "Phase 0 - Software Foundation",
            "api_version": "0.1.0",
            "knowledge_base_version": settings.knowledge_base_version,
        }
    }


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "Phase 0 - Software Foundation",
        "documentation": "/docs",
        "endpoints": {
            "health": "/health",
            "readiness": "/ready",
            "version": "/version",
            "api_v1": "/v1",
        },
    }
