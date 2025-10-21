"""
Test cases for repository layer.

This module tests the ClientRepository and ensures proper
data access patterns and CRUD operations.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ClientUpdate


@pytest.mark.asyncio
class TestClientRepositoryAsync:
    """Test suite for async ClientRepository operations."""

    async def test_create_async(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test creating a client asynchronously."""
        repo = ClientRepository(async_test_db)
        client_create = ClientCreate(**sample_client_data)

        client = await repo.create_async(client_create)

        assert client.id is not None
        assert client.full_name == sample_client_data["full_name"]
        assert client.email == sample_client_data["email"]

    async def test_get_by_id_async(
        self, async_test_db: AsyncSession, sample_client_in_db: Client
    ):
        """Test retrieving client by ID asynchronously."""
        repo = ClientRepository(async_test_db)

        client = await repo.get_by_id_async(sample_client_in_db.id)

        assert client is not None
        assert client.id == sample_client_in_db.id
        assert client.email == sample_client_in_db.email

    async def test_get_by_id_async_not_found(self, async_test_db: AsyncSession):
        """Test retrieving non-existent client returns None."""
        repo = ClientRepository(async_test_db)

        client = await repo.get_by_id_async(99999)

        assert client is None

    async def test_get_by_email_async(
        self, async_test_db: AsyncSession, sample_client_in_db: Client
    ):
        """Test retrieving client by email asynchronously."""
        repo = ClientRepository(async_test_db)

        client = await repo.get_by_email_async(sample_client_in_db.email)

        assert client is not None
        assert client.email == sample_client_in_db.email
        assert client.id == sample_client_in_db.id

    async def test_get_by_email_async_not_found(self, async_test_db: AsyncSession):
        """Test retrieving non-existent email returns None."""
        repo = ClientRepository(async_test_db)

        client = await repo.get_by_email_async("nonexistent@example.com")

        assert client is None

    async def test_get_all_async(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test retrieving all clients with pagination."""
        repo = ClientRepository(async_test_db)

        # Create multiple clients
        for i in range(5):
            data = sample_client_data.copy()
            data["email"] = f"user{i}@example.com"
            client_create = ClientCreate(**data)
            await repo.create_async(client_create)

        # Get all clients
        clients = await repo.get_all_async(skip=0, limit=10)

        assert len(clients) == 5

    async def test_get_all_async_pagination(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test pagination in get_all."""
        repo = ClientRepository(async_test_db)

        # Create 5 clients
        for i in range(5):
            data = sample_client_data.copy()
            data["email"] = f"user{i}@example.com"
            client_create = ClientCreate(**data)
            await repo.create_async(client_create)

        # Test pagination
        first_page = await repo.get_all_async(skip=0, limit=2)
        second_page = await repo.get_all_async(skip=2, limit=2)

        assert len(first_page) == 2
        assert len(second_page) == 2
        assert first_page[0].id != second_page[0].id

    async def test_update_async(
        self, async_test_db: AsyncSession, sample_client_in_db: Client
    ):
        """Test updating client asynchronously."""
        repo = ClientRepository(async_test_db)

        update_data = ClientUpdate(
            full_name="Updated Name", company="New Company"
        )

        updated_client = await repo.update_async(sample_client_in_db.id, update_data)

        assert updated_client is not None
        assert updated_client.full_name == "Updated Name"
        assert updated_client.company == "New Company"
        assert updated_client.email == sample_client_in_db.email  # Unchanged

    async def test_update_async_not_found(self, async_test_db: AsyncSession):
        """Test updating non-existent client returns None."""
        repo = ClientRepository(async_test_db)
        update_data = ClientUpdate(full_name="Updated Name")

        result = await repo.update_async(99999, update_data)

        assert result is None

    async def test_delete_async(
        self, async_test_db: AsyncSession, sample_client_in_db: Client
    ):
        """Test deleting client asynchronously."""
        repo = ClientRepository(async_test_db)

        result = await repo.delete_async(sample_client_in_db.id)

        assert result is True

        # Verify deletion
        deleted_client = await repo.get_by_id_async(sample_client_in_db.id)
        assert deleted_client is None

    async def test_delete_async_not_found(self, async_test_db: AsyncSession):
        """Test deleting non-existent client returns False."""
        repo = ClientRepository(async_test_db)

        result = await repo.delete_async(99999)

        assert result is False

    async def test_count_async(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test counting clients."""
        repo = ClientRepository(async_test_db)

        # Create 3 clients
        for i in range(3):
            data = sample_client_data.copy()
            data["email"] = f"user{i}@example.com"
            client_create = ClientCreate(**data)
            await repo.create_async(client_create)

        count = await repo.count_async()

        assert count == 3


class TestClientRepositorySync:
    """Test suite for sync ClientRepository operations."""

    def test_create_sync(self, test_db: Session, sample_client_data: dict):
        """Test creating a client synchronously."""
        repo = ClientRepository(test_db)
        client_create = ClientCreate(**sample_client_data)

        client = repo.create(client_create)

        assert client.id is not None
        assert client.full_name == sample_client_data["full_name"]
        assert client.email == sample_client_data["email"]

    def test_get_by_id_sync(self, test_db: Session, sample_client_data: dict):
        """Test retrieving client by ID synchronously."""
        repo = ClientRepository(test_db)
        client_create = ClientCreate(**sample_client_data)
        created_client = repo.create(client_create)

        client = repo.get_by_id(created_client.id)

        assert client is not None
        assert client.id == created_client.id

    def test_get_by_email_sync(self, test_db: Session, sample_client_data: dict):
        """Test retrieving client by email synchronously."""
        repo = ClientRepository(test_db)
        client_create = ClientCreate(**sample_client_data)
        created_client = repo.create(client_create)

        client = repo.get_by_email(created_client.email)

        assert client is not None
        assert client.email == created_client.email

    def test_get_all_sync(self, test_db: Session, sample_client_data: dict):
        """Test retrieving all clients synchronously."""
        repo = ClientRepository(test_db)

        # Create multiple clients
        for i in range(3):
            data = sample_client_data.copy()
            data["email"] = f"user{i}@example.com"
            client_create = ClientCreate(**data)
            repo.create(client_create)

        clients = repo.get_all(skip=0, limit=10)

        assert len(clients) == 3

    def test_update_sync(self, test_db: Session, sample_client_data: dict):
        """Test updating client synchronously."""
        repo = ClientRepository(test_db)
        client_create = ClientCreate(**sample_client_data)
        created_client = repo.create(client_create)

        update_data = ClientUpdate(full_name="Updated Name")
        updated_client = repo.update(created_client.id, update_data)

        assert updated_client is not None
        assert updated_client.full_name == "Updated Name"

    def test_delete_sync(self, test_db: Session, sample_client_data: dict):
        """Test deleting client synchronously."""
        repo = ClientRepository(test_db)
        client_create = ClientCreate(**sample_client_data)
        created_client = repo.create(client_create)

        result = repo.delete(created_client.id)

        assert result is True
        assert repo.get_by_id(created_client.id) is None

    def test_count_sync(self, test_db: Session, sample_client_data: dict):
        """Test counting clients synchronously."""
        repo = ClientRepository(test_db)

        # Create 2 clients
        for i in range(2):
            data = sample_client_data.copy()
            data["email"] = f"user{i}@example.com"
            client_create = ClientCreate(**data)
            repo.create(client_create)

        count = repo.count()

        assert count == 2

