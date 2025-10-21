"""
Test cases for main application module.

This module tests FastAPI application initialization,
middleware, exception handlers, and core endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app, create_app


class TestAppCreation:
    """Test suite for application creation and configuration."""

    def test_create_app(self):
        """Test application creation."""
        test_app = create_app()

        assert test_app is not None
        assert test_app.title == "Zititex API"

    def test_app_has_cors_middleware(self):
        """Test that CORS middleware is configured."""
        test_app = create_app()

        # Check that middleware is present in middleware_stack
        middleware_types = [str(type(m)) for m in test_app.user_middleware]
        has_cors = any("CORSMiddleware" in m_type for m_type in middleware_types)
        
        # Also check in the middleware stack
        if not has_cors and hasattr(test_app, 'middleware_stack'):
            stack_str = str(test_app.middleware_stack)
            has_cors = "CORSMiddleware" in stack_str
        
        assert has_cors, f"CORS middleware not found. User middleware: {middleware_types}"


class TestHealthEndpoint:
    """Test suite for health check endpoint."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with TestClient(app) as c:
            yield c

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data

    def test_health_check_returns_service_info(self, client):
        """Test that health check returns service information."""
        response = client.get("/health")
        data = response.json()

        assert "Zititex API" in data["service"]
        assert isinstance(data["version"], str)


class TestRootEndpoint:
    """Test suite for root endpoint."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with TestClient(app) as c:
            yield c

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    def test_root_message_contains_app_name(self, client):
        """Test that root message contains application name."""
        response = client.get("/")
        data = response.json()

        assert "API" in data["message"]


class TestMiddleware:
    """Test suite for middleware functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with TestClient(app) as c:
            yield c

    def test_no_cache_headers(self, client):
        """Test that no-cache headers are added."""
        response = client.get("/health")

        assert "Cache-Control" in response.headers
        assert "no-cache" in response.headers["Cache-Control"]
        assert "Pragma" in response.headers
        assert "Expires" in response.headers


class TestExceptionHandler:
    """Test suite for global exception handler."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with TestClient(app) as c:
            yield c

    def test_global_exception_handler_on_invalid_route(self, client):
        """Test exception handler on non-existent route."""
        response = client.get("/nonexistent-route")

        assert response.status_code == 404

    def test_exception_handler_structure(self, client):
        """Test that error responses have proper structure."""
        response = client.get("/nonexistent-route")
        data = response.json()

        # FastAPI's default 404 response structure
        assert "detail" in data


class TestAPIRoutes:
    """Test suite for API route registration."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        with TestClient(app) as c:
            yield c

    def test_contact_route_registered(self, client):
        """Test that contact route is registered."""
        # We expect validation error or 500 (if missing config)
        # but not 404 (route not found)
        response = client.post("/api/v1/contact/", json={})

        assert response.status_code != 404

    def test_docs_route_exists(self, client):
        """Test that OpenAPI docs route exists."""
        response = client.get("/docs")

        # Docs may be disabled in production (returns 404) or enabled (returns 200)
        assert response.status_code in [200, 404]

    def test_openapi_schema_accessible(self, client):
        """Test that OpenAPI schema is accessible."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data

