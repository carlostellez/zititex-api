"""
Pytest configuration and fixtures.

This module provides shared fixtures and configuration for all tests,
including database setup, test client, and mock services.
"""

import os
from typing import AsyncGenerator, Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.core.database import Base, get_async_db, get_db
from app.main import app
from app.models.client import Client

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
TEST_ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


# Synchronous test engine and session
@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    # Clean up database file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
def test_db(test_engine) -> Generator[Session, None, None]:
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Asynchronous test engine and session
@pytest.fixture(scope="function")
async def async_test_engine():
    """Create an async test database engine."""
    engine = create_async_engine(
        TEST_ASYNC_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

    # Clean up database file
    if os.path.exists("./test.db"):
        os.remove("./test.db")


@pytest.fixture(scope="function")
async def async_test_db(
    async_test_engine,
) -> AsyncGenerator[AsyncSession, None]:
    """Create an async test database session."""
    AsyncTestingSessionLocal = async_sessionmaker(
        async_test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    async with AsyncTestingSessionLocal() as session:
        yield session
        # Rollback any uncommitted changes after test
        await session.rollback()


# Test client fixtures
@pytest.fixture(scope="function")
def client(test_db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database dependency override.

    This fixture provides a synchronous test client for testing API endpoints.
    """

    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def async_client(
    async_test_db: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Create an async test client with database dependency override.

    This fixture provides an asynchronous test client for testing async endpoints.
    """

    async def override_get_async_db():
        yield async_test_db

    app.dependency_overrides[get_async_db] = override_get_async_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


# Sample data fixtures
@pytest.fixture
def sample_client_data() -> dict:
    """Sample client data for testing."""
    return {
        "full_name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "phone": "+52 123 456 7890",
        "company": "Test Company",
        "product_type": "Textiles",
        "quantity": "Más de 10,000 unidades (opcional)",
        "message": "This is a test message for contact form submission.",
    }


@pytest.fixture
def sample_client_minimal_data() -> dict:
    """Sample minimal client data for testing."""
    return {
        "full_name": "Maria Garcia",
        "email": "maria@example.com",
        "phone": "1234567890",
        "message": "Minimal test message.",
    }


@pytest.fixture
async def sample_client_in_db(
    async_test_db: AsyncSession, sample_client_data: dict
) -> Client:
    """Create a sample client in the database."""
    client = Client(**sample_client_data)
    async_test_db.add(client)
    await async_test_db.commit()
    await async_test_db.refresh(client)
    return client


# Mock fixtures
@pytest.fixture
def mock_mailgun_service(monkeypatch):
    """Mock the Mailgun service for testing."""
    mock_service = MagicMock()
    mock_service.send_contact_form_email.return_value = True
    mock_service.send_email.return_value = {"id": "test-message-id"}

    from app.services import mailgun

    monkeypatch.setattr(mailgun, "mailgun_service", mock_service)
    return mock_service


@pytest.fixture
def mock_settings_with_email(monkeypatch):
    """Mock settings with email configuration."""
    monkeypatch.setattr(settings, "mailgun_api_key", "test-api-key")
    monkeypatch.setattr(settings, "mailgun_domain", "test.mailgun.org")
    monkeypatch.setattr(settings, "admin_email", "admin@test.com")
    return settings


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "asyncio: mark test as async")

