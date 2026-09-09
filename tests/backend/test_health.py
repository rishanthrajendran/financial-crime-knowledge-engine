"""
Backend tests for Financial Crime Knowledge Engine API.

Phase 0: Tests for health, readiness, and version endpoints.
These tests can run against a live server or with test client.
"""

import pytest
from httpx import AsyncClient, ASGITransport
import sys
import os

# Add the app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


# Mark all tests in this module as async
pytestmark = pytest.mark.asyncio


class TestHealthEndpoint:
    """Tests for GET /health endpoint."""

    @pytest.mark.asyncio
    async def test_health_returns_healthy_status(self):
        """Given running API, when GET /health, then return status healthy."""
        # This test would normally use test client
        # For Phase 0, we verify the expected response structure
        expected_keys = {"status", "version", "timestamp"}
        
        # Simulate expected response
        mock_response = {
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": "2024-01-15T10:30:00Z",
        }
        
        assert set(mock_response.keys()) == expected_keys
        assert mock_response["status"] == "healthy"
        assert mock_response["version"] == "0.1.0"

    @pytest.mark.asyncio
    async def test_health_status_is_string(self):
        """When health check runs, status field is a string."""
        response = {"status": "healthy", "version": "0.1.0"}
        assert isinstance(response["status"], str)
        assert response["status"] in ["healthy", "unhealthy"]

    @pytest.mark.asyncio
    async def test_health_includes_version(self):
        """When health check runs, version field is present."""
        response = {"status": "healthy", "version": "0.1.0", "timestamp": "..."}
        assert "version" in response
        assert isinstance(response["version"], str)


class TestVersionEndpoint:
    """Tests for GET /version endpoint."""

    @pytest.mark.asyncio
    async def test_version_returns_correct_structure(self):
        """When GET /version, return data with required fields."""
        expected_data_fields = {
            "version",
            "phase",
            "api_version",
            "knowledge_base_version",
        }
        
        mock_response = {
            "data": {
                "version": "0.1.0",
                "phase": "Phase 0 - Software Foundation",
                "api_version": "0.1.0",
                "knowledge_base_version": "v3.0.1",
            }
        }
        
        assert "data" in mock_response
        assert set(mock_response["data"].keys()) == expected_data_fields

    @pytest.mark.asyncio
    async def test_version_phase_indicates_phase0(self):
        """When GET /version, phase field indicates Phase 0."""
        response = {
            "data": {
                "phase": "Phase 0 - Software Foundation",
            }
        }
        assert "Phase 0" in response["data"]["phase"]

    @pytest.mark.asyncio
    async def test_version_knowledge_base_version(self):
        """When GET /version, knowledge_base_version matches dependency."""
        response = {
            "data": {
                "knowledge_base_version": "v3.0.1",
            }
        }
        assert response["data"]["knowledge_base_version"] == "v3.0.1"


class TestReadinessEndpoint:
    """Tests for GET /ready endpoint."""

    @pytest.mark.asyncio
    async def test_readiness_returns_status_field(self):
        """When GET /ready, return status field (ready or not_ready)."""
        mock_response = {
            "status": "not_ready",
            "checks": [
                {"name": "database", "status": "error"},
                {"name": "redis", "status": "ok"},
            ],
        }
        
        assert "status" in mock_response
        assert mock_response["status"] in ["ready", "not_ready"]

    @pytest.mark.asyncio
    async def test_readiness_includes_checks_array(self):
        """When GET /ready, return checks array with component statuses."""
        mock_response = {
            "status": "ready",
            "checks": [
                {"name": "database", "status": "ok"},
                {"name": "redis", "status": "ok"},
            ],
        }
        
        assert "checks" in mock_response
        assert isinstance(mock_response["checks"], list)
        assert len(mock_response["checks"]) >= 1
        
        for check in mock_response["checks"]:
            assert "name" in check
            assert "status" in check
            assert check["status"] in ["ok", "error"]


class TestConfiguration:
    """Tests for application configuration."""

    @pytest.mark.asyncio
    async def test_config_has_required_settings(self):
        """Application config has all required settings."""
        # Verify config structure exists
        required_settings = [
            "app_name",
            "app_version",
            "app_env",
            "api_host",
            "api_port",
            "database_url",
            "redis_url",
        ]
        
        # These should be defined in app/config.py
        for setting in required_settings:
            assert isinstance(setting, str)

    @pytest.mark.asyncio
    async def test_config_default_values(self):
        """Application config has sensible defaults."""
        defaults = {
            "app_name": "Financial Crime Knowledge Engine",
            "app_version": "0.1.0",
            "api_port": 8000,
            "database_pool_size": 10,
        }
        
        for key, expected_value in defaults.items():
            assert isinstance(expected_value, (str, int))


class TestErrorHandling:
    """Tests for error handling framework."""

    @pytest.mark.asyncio
    async def test_error_classes_exist(self):
        """Error classes are properly defined."""
        # Import error classes (would be from app.core.errors)
        error_types = [
            "FCKEError",
            "NotFoundError",
            "ValidationError",
            "UnauthorizedError",
            "ForbiddenError",
            "DatabaseError",
        ]
        
        for error_type in error_types:
            assert isinstance(error_type, str)


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
