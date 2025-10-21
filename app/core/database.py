"""
Database configuration and session management.

This module provides database connection setup, session management,
and base model classes using SQLAlchemy.
"""

from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Create declarative base for models
Base = declarative_base()


def get_database_url() -> str:
    """
    Construct synchronous database URL from settings.

    Returns:
        MySQL database URL for sync operations
    """
    if settings.database_url:
        return settings.database_url

    return (
        f"mysql+pymysql://{settings.mysql_user}:{settings.mysql_password}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}"
    )


def get_async_database_url() -> str:
    """
    Construct asynchronous database URL from settings.

    Returns:
        MySQL database URL for async operations
    """
    if settings.database_async_url:
        return settings.database_async_url

    return (
        f"mysql+aiomysql://{settings.mysql_user}:{settings.mysql_password}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_database}"
    )


# Create synchronous engine
engine = create_engine(
    get_database_url(),
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create synchronous session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create asynchronous engine
async_engine = create_async_engine(
    get_async_database_url(),
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create asynchronous session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for synchronous database sessions.

    Yields:
        Database session

    Example:
        @app.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for asynchronous database sessions.

    Yields:
        Async database session

    Example:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_async_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """
    Create all database tables.

    This should be called on application startup in development.
    In production, use Alembic migrations instead.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    """
    Drop all database tables.

    WARNING: This will delete all data. Use with caution.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

