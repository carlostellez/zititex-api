"""
Client repository for database operations.

This module implements the Repository Pattern for Client entity operations,
providing clean separation between business logic and data access.
"""

from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class ClientRepository:
    """
    Repository for Client database operations.

    This class implements the Repository Pattern, providing a clean interface
    for all database operations related to the Client entity. It supports both
    synchronous and asynchronous operations.

    Design Patterns:
        - Repository Pattern: Abstracts data access logic
        - Dependency Injection: Database session injected via constructor

    SOLID Principles:
        - Single Responsibility: Only handles Client data access
        - Dependency Inversion: Depends on abstractions (Session interface)
    """

    def __init__(self, db: Session | AsyncSession):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy session (sync or async)
        """
        self.db = db
        self.is_async = isinstance(db, AsyncSession)

    async def create_async(self, client_data: ClientCreate) -> Client:
        """
        Create a new client record asynchronously.

        Args:
            client_data: Client creation data

        Returns:
            Created client instance

        Example:
            >>> repo = ClientRepository(async_db)
            >>> client = await repo.create_async(ClientCreate(...))
        """
        client = Client(**client_data.model_dump())
        self.db.add(client)
        await self.db.commit()
        await self.db.refresh(client)
        return client

    def create(self, client_data: ClientCreate) -> Client:
        """
        Create a new client record synchronously.

        Args:
            client_data: Client creation data

        Returns:
            Created client instance

        Example:
            >>> repo = ClientRepository(db)
            >>> client = repo.create(ClientCreate(...))
        """
        client = Client(**client_data.model_dump())
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    async def get_by_id_async(self, client_id: int) -> Optional[Client]:
        """
        Get client by ID asynchronously.

        Args:
            client_id: Client ID

        Returns:
            Client instance or None if not found
        """
        result = await self.db.execute(select(Client).where(Client.id == client_id))
        return result.scalar_one_or_none()

    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Get client by ID synchronously.

        Args:
            client_id: Client ID

        Returns:
            Client instance or None if not found
        """
        result = self.db.execute(select(Client).where(Client.id == client_id))
        return result.scalar_one_or_none()

    async def get_by_email_async(self, email: str) -> Optional[Client]:
        """
        Get client by email asynchronously.

        Args:
            email: Client email address

        Returns:
            Client instance or None if not found
        """
        result = await self.db.execute(select(Client).where(Client.email == email))
        return result.scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[Client]:
        """
        Get client by email synchronously.

        Args:
            email: Client email address

        Returns:
            Client instance or None if not found
        """
        result = self.db.execute(select(Client).where(Client.email == email))
        return result.scalar_one_or_none()

    async def get_all_async(
        self, skip: int = 0, limit: int = 100
    ) -> List[Client]:
        """
        Get all clients with pagination asynchronously.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of client instances
        """
        result = await self.db.execute(
            select(Client).offset(skip).limit(limit).order_by(Client.created_at.desc())
        )
        return list(result.scalars().all())

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        """
        Get all clients with pagination synchronously.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of client instances
        """
        result = self.db.execute(
            select(Client).offset(skip).limit(limit).order_by(Client.created_at.desc())
        )
        return list(result.scalars().all())

    async def update_async(
        self, client_id: int, client_data: ClientUpdate
    ) -> Optional[Client]:
        """
        Update client record asynchronously.

        Args:
            client_id: Client ID
            client_data: Update data

        Returns:
            Updated client instance or None if not found
        """
        client = await self.get_by_id_async(client_id)
        if not client:
            return None

        update_dict = client_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(client, key, value)

        await self.db.commit()
        await self.db.refresh(client)
        return client

    def update(
        self, client_id: int, client_data: ClientUpdate
    ) -> Optional[Client]:
        """
        Update client record synchronously.

        Args:
            client_id: Client ID
            client_data: Update data

        Returns:
            Updated client instance or None if not found
        """
        client = self.get_by_id(client_id)
        if not client:
            return None

        update_dict = client_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(client, key, value)

        self.db.commit()
        self.db.refresh(client)
        return client

    async def delete_async(self, client_id: int) -> bool:
        """
        Delete client record asynchronously.

        Args:
            client_id: Client ID

        Returns:
            True if deleted, False if not found
        """
        client = await self.get_by_id_async(client_id)
        if not client:
            return False

        # Note: delete() is not async in SQLAlchemy 2.0
        await self.db.delete(client)
        await self.db.commit()
        return True

    def delete(self, client_id: int) -> bool:
        """
        Delete client record synchronously.

        Args:
            client_id: Client ID

        Returns:
            True if deleted, False if not found
        """
        client = self.get_by_id(client_id)
        if not client:
            return False

        self.db.delete(client)
        self.db.commit()
        return True

    async def count_async(self) -> int:
        """
        Count total number of clients asynchronously.

        Returns:
            Total count of clients
        """
        result = await self.db.execute(select(Client))
        return len(result.scalars().all())

    def count(self) -> int:
        """
        Count total number of clients synchronously.

        Returns:
            Total count of clients
        """
        result = self.db.execute(select(func.count()).select_from(Client))
        return result.scalar()

