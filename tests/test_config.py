"""
Test cases for configuration module.

This module tests application settings, environment variable
loading, and database URL construction.
"""

from unittest.mock import patch

import pytest

from app.core.config import Settings
from app.core.database import get_async_database_url, get_database_url


class TestSettings:
    """Test suite for Settings configuration."""

    def test_default_settings(self):
        """Test default settings values."""
        settings = Settings()

        assert settings.app_name == "Zititex API"
        assert settings.app_version == "0.1.0"
        assert settings.debug is False
        assert settings.host == "0.0.0.0"
        assert settings.port == 8000

    def test_database_defaults(self):
        """Test database default settings."""
        settings = Settings()

        assert settings.mysql_host == "localhost"
        assert settings.mysql_port == 3306
        assert settings.mysql_user == "root"
        assert settings.mysql_database == "zititex_db"

    def test_cors_defaults(self):
        """Test CORS default settings."""
        settings = Settings()

        assert settings.allowed_origins == ["*"]
        assert settings.allowed_methods == ["*"]
        assert settings.allowed_headers == ["*"]

    @patch.dict(
        "os.environ",
        {
            "APP_NAME": "Test API",
            "APP_VERSION": "1.0.0",
            "DEBUG": "true",
            "MYSQL_HOST": "testhost",
            "MYSQL_PORT": "3307",
        },
    )
    def test_settings_from_env(self):
        """Test loading settings from environment variables."""
        settings = Settings()

        assert settings.app_name == "Test API"
        assert settings.app_version == "1.0.0"
        assert settings.debug is True
        assert settings.mysql_host == "testhost"
        assert settings.mysql_port == 3307


class TestDatabaseURL:
    """Test suite for database URL construction."""

    def test_get_database_url_from_settings(self):
        """Test constructing database URL from individual settings."""
        with patch("app.core.database.settings") as mock_settings:
            mock_settings.database_url = None
            mock_settings.mysql_user = "testuser"
            mock_settings.mysql_password = "testpass"
            mock_settings.mysql_host = "testhost"
            mock_settings.mysql_port = 3306
            mock_settings.mysql_database = "testdb"

            url = get_database_url()

            assert "mysql+pymysql://" in url
            assert "testuser" in url
            assert "testpass" in url
            assert "testhost" in url
            assert "testdb" in url

    def test_get_database_url_from_direct_setting(self):
        """Test using direct database_url setting."""
        with patch("app.core.database.settings") as mock_settings:
            mock_settings.database_url = "mysql://custom:url@host/db"

            url = get_database_url()

            assert url == "mysql://custom:url@host/db"

    def test_get_async_database_url_from_settings(self):
        """Test constructing async database URL from individual settings."""
        with patch("app.core.database.settings") as mock_settings:
            mock_settings.database_async_url = None
            mock_settings.mysql_user = "testuser"
            mock_settings.mysql_password = "testpass"
            mock_settings.mysql_host = "testhost"
            mock_settings.mysql_port = 3306
            mock_settings.mysql_database = "testdb"

            url = get_async_database_url()

            assert "mysql+aiomysql://" in url
            assert "testuser" in url
            assert "testpass" in url
            assert "testhost" in url
            assert "testdb" in url

    def test_get_async_database_url_from_direct_setting(self):
        """Test using direct database_async_url setting."""
        with patch("app.core.database.settings") as mock_settings:
            mock_settings.database_async_url = "mysql+aiomysql://custom:url@host/db"

            url = get_async_database_url()

            assert url == "mysql+aiomysql://custom:url@host/db"

