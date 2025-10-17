"""Test health endpoints."""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient


class TestHealthEndpoints:
    """Test health check endpoints."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    @pytest.mark.asyncio
    async def test_health_check_async(self, async_client: AsyncClient) -> None:
        """Test health check endpoint (async)."""
        response = await async_client.get("/v1/health/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Service is healthy"

    @pytest.mark.asyncio
    async def test_liveness(self, async_client: AsyncClient) -> None:
        """Test liveness endpoint."""
        response = await async_client.get("/v1/health/liveness")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Service is alive"

    @pytest.mark.asyncio
    async def test_readiness(self, async_client: AsyncClient) -> None:
        """Test readiness endpoint."""
        response = await async_client.get("/v1/health/readiness")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Service is ready"

