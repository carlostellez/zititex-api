"""Test domain entities."""

from datetime import datetime
from uuid import UUID

import pytest

from src.domain.entities.base import BaseEntity


class TestBaseEntity:
    """Test BaseEntity class."""

    def test_base_entity_creation(self) -> None:
        """Test creating a base entity."""
        entity = BaseEntity()

        assert isinstance(entity.id, UUID)
        assert isinstance(entity.created_at, datetime)
        assert entity.updated_at is None
        assert entity.is_active is True

    def test_base_entity_with_custom_values(self) -> None:
        """Test creating a base entity with custom values."""
        custom_time = datetime(2024, 1, 1, 12, 0, 0)
        entity = BaseEntity(
            created_at=custom_time, updated_at=custom_time, is_active=False
        )

        assert isinstance(entity.id, UUID)
        assert entity.created_at == custom_time
        assert entity.updated_at == custom_time
        assert entity.is_active is False

    def test_base_entity_json_serialization(self) -> None:
        """Test JSON serialization of base entity."""
        entity = BaseEntity()
        entity_dict = entity.model_dump()

        assert "id" in entity_dict
        assert "created_at" in entity_dict
        assert "updated_at" in entity_dict
        assert "is_active" in entity_dict

