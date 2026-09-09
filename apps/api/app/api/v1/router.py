"""
API v1 Router

Organizes all v1 API endpoints. Currently empty as business
endpoints will be added in Phase 1+.
"""

from fastapi import APIRouter

# Create main v1 router
router = APIRouter(prefix="/v1", tags=["v1"])

# Import and include sub-routers here as they are created
# Example:
# from app.api.v1.endpoints import knowledge, users
# router.include_router(knowledge.router)
# router.include_router(users.router)

# Placeholder for future endpoints
@router.get("/")
async def v1_root() -> dict[str, object]:
    """API v1 root - returns available endpoint groups."""
    return {
        "message": "Financial Crime Knowledge Engine API v1",
        "version": "0.1.0",
        "status": "Phase 0 - Foundation only",
        "endpoints": {
            # Endpoints will be listed here as they're implemented
            "knowledge": "/v1/knowledge (planned)",
            "documents": "/v1/documents (planned)",
            "assessments": "/v1/assessments (planned)",
            "users": "/v1/users (planned)",
        },
    }
