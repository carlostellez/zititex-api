"""
Test cases for Pydantic schemas.

This module tests schema validation, serialization,
and deserialization for all data models.
"""

import pytest
from pydantic import ValidationError

from app.schemas.client import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
    ContactForm,
    ContactResponse,
)


class TestContactFormSchema:
    """Test suite for ContactForm schema."""

    def test_valid_contact_form_full(self):
        """Test valid contact form with all fields."""
        data = {
            "full_name": "Juan Pérez",
            "email": "juan@example.com",
            "phone": "+52 123 456 7890",
            "company": "Test Corp",
            "product_type": "Textiles",
            "quantity": 100,
            "message": "This is a test message.",
        }

        form = ContactForm(**data)

        assert form.full_name == data["full_name"]
        assert form.email == data["email"]
        assert form.company == data["company"]
        assert form.quantity == data["quantity"]

    def test_valid_contact_form_minimal(self):
        """Test valid contact form with only required fields."""
        data = {
            "full_name": "Maria Garcia",
            "email": "maria@example.com",
            "phone": "1234567890",
            "message": "Minimal test message.",
        }

        form = ContactForm(**data)

        assert form.full_name == data["full_name"]
        assert form.company is None
        assert form.product_type is None
        assert form.quantity is None

    def test_invalid_email(self):
        """Test that invalid email raises validation error."""
        data = {
            "full_name": "Test User",
            "email": "invalid-email",
            "phone": "1234567890",
            "message": "Test message",
        }

        with pytest.raises(ValidationError) as exc_info:
            ContactForm(**data)

        assert "email" in str(exc_info.value).lower()

    def test_short_name(self):
        """Test that too short name raises validation error."""
        data = {
            "full_name": "A",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Test message",
        }

        with pytest.raises(ValidationError) as exc_info:
            ContactForm(**data)

        assert "full_name" in str(exc_info.value).lower()

    def test_short_message(self):
        """Test that too short message raises validation error."""
        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Short",
        }

        with pytest.raises(ValidationError) as exc_info:
            ContactForm(**data)

        assert "message" in str(exc_info.value).lower()

    def test_phone_validation_no_digits(self):
        """Test phone validation with no digits."""
        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "abcdefghij",
            "message": "Test message for validation",
        }

        with pytest.raises(ValidationError) as exc_info:
            ContactForm(**data)

        assert "phone" in str(exc_info.value).lower()

    def test_phone_validation_with_separators(self):
        """Test phone validation accepts separators."""
        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "+52 (123) 456-7890",
            "message": "Test message for validation",
        }

        form = ContactForm(**data)
        assert form.phone == data["phone"]

    def test_negative_quantity(self):
        """Test that negative quantity raises validation error."""
        data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "quantity": -5,
            "message": "Test message",
        }

        with pytest.raises(ValidationError) as exc_info:
            ContactForm(**data)

        assert "quantity" in str(exc_info.value).lower()


class TestContactResponseSchema:
    """Test suite for ContactResponse schema."""

    def test_valid_response(self):
        """Test valid contact response."""
        data = {
            "success": True,
            "message": "Success message",
            "data": {"key": "value"},
        }

        response = ContactResponse(**data)

        assert response.success is True
        assert response.message == data["message"]
        assert response.data == data["data"]

    def test_response_with_empty_data(self):
        """Test response with empty data dict."""
        data = {
            "success": False,
            "message": "Error message",
        }

        response = ContactResponse(**data)

        assert response.success is False
        assert response.data == {}


class TestClientCreateSchema:
    """Test suite for ClientCreate schema."""

    def test_valid_client_create(self):
        """Test valid client creation schema."""
        data = {
            "full_name": "Test Client",
            "email": "client@example.com",
            "phone": "1234567890",
            "message": "Test message",
            "company": "Test Co",
            "product_type": "Type A",
            "quantity": 50,
        }

        client_create = ClientCreate(**data)

        assert client_create.full_name == data["full_name"]
        assert client_create.company == data["company"]

    def test_client_create_minimal(self):
        """Test client creation with minimal fields."""
        data = {
            "full_name": "Test Client",
            "email": "client@example.com",
            "phone": "1234567890",
            "message": "Test message",
        }

        client_create = ClientCreate(**data)

        assert client_create.full_name == data["full_name"]
        assert client_create.company is None


class TestClientUpdateSchema:
    """Test suite for ClientUpdate schema."""

    def test_partial_update(self):
        """Test partial update with only some fields."""
        data = {
            "full_name": "Updated Name",
            "company": "Updated Company",
        }

        client_update = ClientUpdate(**data)

        assert client_update.full_name == data["full_name"]
        assert client_update.company == data["company"]
        assert client_update.email is None

    def test_empty_update(self):
        """Test update with no fields."""
        client_update = ClientUpdate()

        assert client_update.full_name is None
        assert client_update.email is None


class TestClientResponseSchema:
    """Test suite for ClientResponse schema."""

    def test_client_response_from_orm(self, sample_client_in_db):
        """Test creating response from ORM model."""
        # This would typically use model_validate in real scenario
        data = {
            "id": 1,
            "full_name": "Test Client",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Test message",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }

        response = ClientResponse(**data)

        assert response.id == data["id"]
        assert response.full_name == data["full_name"]

