"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from src.domain.entities.base import BaseEntity

EntityType = TypeVar("EntityType", bound=BaseEntity)


class BaseRepository(ABC, Generic[EntityType]):
    """Base repository interface for CRUD operations."""

    @abstractmethod
    async def create(self, entity: EntityType) -> EntityType:
        """Create a new entity."""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Optional[EntityType]:
        """Get entity by ID."""
        pass

    @abstractmethod
    async def get_all(
        self, skip: int = 0, limit: int = 100
    ) -> List[EntityType]:
        """Get all entities with pagination."""
        pass

    @abstractmethod
    async def update(self, entity: EntityType) -> EntityType:
        """Update an existing entity."""
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity by ID."""
        pass

