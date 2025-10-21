"""
Core application configuration and utilities.

This package contains core functionality including configuration,
database setup, and shared utilities.
"""

from app.core.config import settings
from app.core.database import Base, async_engine, engine, get_async_db, get_db

__all__ = [
    "settings",
    "Base",
    "engine",
    "async_engine",
    "get_db",
    "get_async_db",
]

