"""
Test cases for database models.

This module tests the SQLAlchemy models including Client model
and ensures proper database schema and constraints.
"""

from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.client import Client


@pytest.mark.asyncio
class TestClientModel:
    """Test suite for Client model."""

    async def test_create_client_with_all_fields(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test creating a client with all fields."""
        client = Client(**sample_client_data)
        async_test_db.add(client)
        await async_test_db.commit()
        await async_test_db.refresh(client)

        assert client.id is not None
        assert client.full_name == sample_client_data["full_name"]
        assert client.email == sample_client_data["email"]
        assert client.phone == sample_client_data["phone"]
        assert client.company == sample_client_data["company"]
        assert client.product_type == sample_client_data["product_type"]
        assert client.quantity == sample_client_data["quantity"]
        assert client.message == sample_client_data["message"]
        assert isinstance(client.created_at, datetime)
        assert isinstance(client.updated_at, datetime)

    async def test_create_client_with_minimal_fields(
        self, async_test_db: AsyncSession
    ):
        """Test creating a client with only required fields."""
        minimal_data = {
            "full_name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890",
            "message": "Test message",
        }

        client = Client(**minimal_data)
        async_test_db.add(client)
        await async_test_db.commit()
        await async_test_db.refresh(client)

        assert client.id is not None
        assert client.full_name == minimal_data["full_name"]
        assert client.email == minimal_data["email"]
        assert client.company is None
        assert client.product_type is None
        assert client.quantity is None

    async def test_client_repr(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test Client string representation."""
        client = Client(**sample_client_data)
        async_test_db.add(client)
        await async_test_db.commit()
        await async_test_db.refresh(client)

        repr_str = repr(client)
        assert "Client" in repr_str
        assert str(client.id) in repr_str
        assert client.full_name in repr_str
        assert client.email in repr_str

    async def test_client_to_dict(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test converting Client to dictionary."""
        client = Client(**sample_client_data)
        async_test_db.add(client)
        await async_test_db.commit()
        await async_test_db.refresh(client)

        client_dict = client.to_dict()

        assert client_dict["id"] == client.id
        assert client_dict["full_name"] == sample_client_data["full_name"]
        assert client_dict["email"] == sample_client_data["email"]
        assert client_dict["phone"] == sample_client_data["phone"]
        assert client_dict["company"] == sample_client_data["company"]
        assert client_dict["product_type"] == sample_client_data["product_type"]
        assert client_dict["quantity"] == sample_client_data["quantity"]
        assert client_dict["message"] == sample_client_data["message"]
        assert isinstance(client_dict["created_at"], str)
        assert isinstance(client_dict["updated_at"], str)

    async def test_client_timestamps(
        self, async_test_db: AsyncSession, sample_client_data: dict
    ):
        """Test that timestamps are automatically set."""
        client = Client(**sample_client_data)
        async_test_db.add(client)
        await async_test_db.commit()
        await async_test_db.refresh(client)

        assert client.created_at is not None
        assert client.updated_at is not None
        assert isinstance(client.created_at, datetime)
        assert isinstance(client.updated_at, datetime)

    async def test_multiple_clients(
        self, async_test_db: AsyncSession
    ):
        """Test creating multiple client records."""
        clients_data = [
            {
                "full_name": f"User {i}",
                "email": f"user{i}@example.com",
                "phone": f"12345678{i}",
                "message": f"Message {i}",
            }
            for i in range(3)
        ]

        for data in clients_data:
            client = Client(**data)
            async_test_db.add(client)

        await async_test_db.commit()

        # Verify all clients were created with unique IDs
        from sqlalchemy import select

        result = await async_test_db.execute(select(Client))
        all_clients = result.scalars().all()

        assert len(all_clients) == 3
        ids = [c.id for c in all_clients]
        assert len(ids) == len(set(ids))  # All IDs are unique

