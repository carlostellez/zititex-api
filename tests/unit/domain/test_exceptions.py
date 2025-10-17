"""Test domain exceptions."""

import pytest

from src.domain.exceptions import (
    DomainException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    ValidationException,
)


class TestDomainExceptions:
    """Test domain exceptions."""

    def test_domain_exception(self) -> None:
        """Test DomainException."""
        with pytest.raises(DomainException):
            raise DomainException("Test exception")

    def test_entity_not_found_exception(self) -> None:
        """Test EntityNotFoundException."""
        with pytest.raises(EntityNotFoundException) as exc_info:
            raise EntityNotFoundException("User", "123")

        assert exc_info.value.entity_name == "User"
        assert exc_info.value.entity_id == "123"
        assert "User with id 123 not found" in str(exc_info.value)

    def test_entity_already_exists_exception(self) -> None:
        """Test EntityAlreadyExistsException."""
        with pytest.raises(EntityAlreadyExistsException) as exc_info:
            raise EntityAlreadyExistsException("User", "email", "test@example.com")

        assert exc_info.value.entity_name == "User"
        assert exc_info.value.field == "email"
        assert exc_info.value.value == "test@example.com"
        assert "User with email=test@example.com already exists" in str(exc_info.value)

    def test_validation_exception(self) -> None:
        """Test ValidationException."""
        with pytest.raises(ValidationException) as exc_info:
            raise ValidationException("Invalid input")

        assert "Invalid input" in str(exc_info.value)

