"""Test main application."""

from fastapi.testclient import TestClient


class TestMainApplication:
    """Test main application endpoints."""

    def test_api_docs_available(self, client: TestClient) -> None:
        """Test API documentation is available."""
        response = client.get("/v1/docs")
        assert response.status_code == 200

    def test_openapi_schema_available(self, client: TestClient) -> None:
        """Test OpenAPI schema is available."""
        response = client.get("/v1/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Zititex API"

