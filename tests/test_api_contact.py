"""
Test cases for Contact API endpoints.

This module tests the contact form submission endpoint including
database integration, email service, and error handling.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client
from app.repositories.client_repository import ClientRepository


@pytest.mark.asyncio
class TestContactAPI:
    """Test suite for contact form API endpoint."""

    async def test_submit_contact_form_success(
        self,
        async_client: AsyncClient,
        async_test_db: AsyncSession,
        mock_mailgun_service,
        mock_settings_with_email,
        sample_client_data: dict,
    ):
        """Test successful contact form submission."""
        response = await async_client.post("/api/v1/contact/", json=sample_client_data)

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "mensaje enviado exitosamente" in data["message"].lower()
        assert "email" in data["data"]
        assert data["data"]["email"] == sample_client_data["email"]

        # Verify data was saved to database
        repo = ClientRepository(async_test_db)
        clients = await repo.get_all_async()
        assert len(clients) == 1
        assert clients[0].email == sample_client_data["email"]

    async def test_submit_contact_form_minimal_data(
        self,
        async_client: AsyncClient,
        async_test_db: AsyncSession,
        mock_mailgun_service,
        mock_settings_with_email,
        sample_client_minimal_data: dict,
    ):
        """Test contact form with only required fields."""
        response = await async_client.post(
            "/api/v1/contact/", json=sample_client_minimal_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Verify data was saved
        repo = ClientRepository(async_test_db)
        client = await repo.get_by_email(sample_client_minimal_data["email"])
        assert client is not None
        assert client.company is None
        assert client.product_type is None

    async def test_submit_contact_form_invalid_email(
        self,
        async_client: AsyncClient,
        mock_mailgun_service,
        mock_settings_with_email,
    ):
        """Test contact form with invalid email."""
        data = {
            "full_name": "Test User",
            "email": "invalid-email",
            "phone": "1234567890",
            "message": "Test message",
        }

        response = await async_client.post("/api/v1/contact/", json=data)

        assert response.status_code == 422  # Validation error

    async def test_submit_contact_form_missing_required_field(
        self,
        async_client: AsyncClient,
        mock_mailgun_service,
        mock_settings_with_email,
    ):
        """Test contact form with missing required field."""
        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            # Missing phone and message
        }

        response = await async_client.post("/api/v1/contact/", json=data)

        assert response.status_code == 422

    async def test_submit_contact_form_email_service_not_configured(
        self, async_client: AsyncClient, monkeypatch
    ):
        """Test error when email service is not configured."""
        from app.core import settings

        monkeypatch.setattr(settings, "mailgun_api_key", None)
        monkeypatch.setattr(settings, "mailgun_domain", None)

        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Test message",
        }

        response = await async_client.post("/api/v1/contact/", json=data)

        assert response.status_code == 500
        assert "email service not configured" in response.json()["detail"].lower()

    async def test_submit_contact_form_admin_email_not_configured(
        self, async_client: AsyncClient, monkeypatch
    ):
        """Test error when admin email is not configured."""
        from app.core import settings

        monkeypatch.setattr(settings, "mailgun_api_key", "test-key")
        monkeypatch.setattr(settings, "mailgun_domain", "test.domain")
        monkeypatch.setattr(settings, "admin_email", None)

        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Test message",
        }

        response = await async_client.post("/api/v1/contact/", json=data)

        assert response.status_code == 500
        assert "admin email not configured" in response.json()["detail"].lower()

    async def test_submit_contact_form_with_all_optional_fields(
        self,
        async_client: AsyncClient,
        async_test_db: AsyncSession,
        mock_mailgun_service,
        mock_settings_with_email,
    ):
        """Test contact form with all optional fields provided."""
        data = {
            "full_name": "Complete User",
            "email": "complete@example.com",
            "phone": "+52 123 456 7890",
            "company": "Complete Corp",
            "product_type": "Premium Textiles",
            "quantity": "Más de 10,000 unidades (opcional)",
            "message": "This is a complete submission with all fields.",
        }

        response = await async_client.post("/api/v1/contact/", json=data)

        assert response.status_code == 200

        # Verify all fields were saved
        repo = ClientRepository(async_test_db)
        client = await repo.get_by_email(data["email"])
        assert client is not None
        assert client.company == data["company"]
        assert client.product_type == data["product_type"]
        assert client.quantity == data["quantity"]

    async def test_submit_contact_form_email_sending_fails(
        self,
        async_client: AsyncClient,
        async_test_db: AsyncSession,
        mock_mailgun_service,
        mock_settings_with_email,
        sample_client_data: dict,
    ):
        """Test that data is saved even if email sending fails."""
        # Configure mock to fail email sending
        mock_mailgun_service.send_contact_form_email.return_value = False

        response = await async_client.post("/api/v1/contact/", json=sample_client_data)

        # Request should still succeed (we don't fail on email error)
        assert response.status_code == 200

        # But data should be saved
        repo = ClientRepository(async_test_db)
        client = await repo.get_by_email(sample_client_data["email"])
        assert client is not None

    async def test_submit_contact_form_database_error(
        self,
        async_client: AsyncClient,
        mock_mailgun_service,
        mock_settings_with_email,
        monkeypatch,
    ):
        """Test error handling when database operation fails."""
        from app.repositories.client_repository import ClientRepository

        async def mock_create_error(*args, **kwargs):
            raise Exception("Database connection error")

        monkeypatch.setattr(ClientRepository, "create_async", mock_create_error)

        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Test message",
        }

        response = await async_client.post("/api/v1/contact/", json=data)

        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()

    async def test_contact_response_includes_client_id(
        self,
        async_client: AsyncClient,
        async_test_db: AsyncSession,
        mock_mailgun_service,
        mock_settings_with_email,
        sample_client_data: dict,
    ):
        """Test that response includes the created client ID."""
        response = await async_client.post("/api/v1/contact/", json=sample_client_data)

        assert response.status_code == 200
        data = response.json()
        assert "id" in data["data"]
        assert isinstance(data["data"]["id"], int)
        assert data["data"]["id"] > 0

    async def test_multiple_submissions_same_email(
        self,
        async_client: AsyncClient,
        async_test_db: AsyncSession,
        mock_mailgun_service,
        mock_settings_with_email,
        sample_client_data: dict,
    ):
        """Test that multiple submissions with same email are allowed."""
        # First submission
        response1 = await async_client.post(
            "/api/v1/contact/", json=sample_client_data
        )
        assert response1.status_code == 200

        # Second submission with same email
        response2 = await async_client.post(
            "/api/v1/contact/", json=sample_client_data
        )
        assert response2.status_code == 200

        # Both should be saved
        repo = ClientRepository(async_test_db)
        clients = await repo.get_all_async()
        assert len(clients) == 2

