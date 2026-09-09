"""
Custom exception classes and error handling for FCKE API.

Provides:
- FCKEError: Base exception class
- Specific exception types for common errors
- Exception handlers for FastAPI
"""

from typing import Any


class FCKEError(Exception):
    """Base exception for all FCKE application errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Convert error to dictionary for API response."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details if self.details else None,
        }


# HTTP 4xx Errors

class ValidationError(FCKEError):
    """Request validation failed."""

    def __init__(
        self,
        message: str = "Validation failed",
        details: dict[str, Any] | None = None,
    ):
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=422,
            details=details,
        )


class NotFoundError(FCKEError):
    """Resource not found."""

    def __init__(self, resource_type: str = "Resource", resource_id: str | None = None):
        message = f"{resource_type} not found"
        if resource_id:
            message += f" with ID '{resource_id}'"
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details={"resource_type": resource_type, "resource_id": resource_id},
        )


class ConflictError(FCKEError):
    """Resource conflict (e.g., duplicate)."""

    def __init__(self, message: str = "Resource conflict"):
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
        )


class UnauthorizedError(FCKEError):
    """Authentication required."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )


class ForbiddenError(FCKEError):
    """Insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
        )


# HTTP 5xx Errors

class DatabaseError(FCKEError):
    """Database operation failed."""

    def __init__(
        self,
        message: str = "Database operation failed",
        original_error: str | None = None,
    ):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=500,
            details={"original_error": original_error} if original_error else None,
        )


class ExternalServiceError(FCKEError):
    """External service call failed."""

    def __init__(self, service: str, message: str = "External service unavailable"):
        super().__init__(
            message=message,
            code=f"{service.upper()}_ERROR",
            status_code=502,
            details={"service": service},
        )


class ConfigurationError(FCKEError):
    """Application misconfiguration."""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(
            message=message,
            code="CONFIGURATION_ERROR",
            status_code=500,
        )
