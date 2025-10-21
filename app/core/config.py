"""
Application configuration using Pydantic settings.

This module provides centralized configuration management with environment
variable support and validation.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # Application settings
    app_name: str = Field(default="Zititex API", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")

    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")

    # AWS settings - These are automatically provided by Lambda runtime
    aws_region: str = Field(
        default="us-east-2", description="AWS region (auto-provided by Lambda)"
    )
    aws_access_key_id: Optional[str] = Field(
        default=None, description="AWS access key ID (auto-provided by Lambda)"
    )
    aws_secret_access_key: Optional[str] = Field(
        default=None, description="AWS secret access key (auto-provided by Lambda)"
    )

    # Mailgun settings
    mailgun_api_key: Optional[str] = Field(default=None, description="Mailgun API key")
    mailgun_domain: Optional[str] = Field(default=None, description="Mailgun domain")
    mailgun_base_url: str = Field(
        default="https://api.mailgun.net/v3", description="Mailgun base URL"
    )
    admin_email: Optional[str] = Field(
        default=None, description="Admin email for contact form notifications"
    )

    # Database settings (MySQL)
    database_url: Optional[str] = Field(
        default=None, description="Database connection URL (for sync operations)"
    )
    database_async_url: Optional[str] = Field(
        default=None, description="Async database connection URL"
    )
    mysql_host: str = Field(default="localhost", description="MySQL host")
    mysql_port: int = Field(default=3306, description="MySQL port")
    mysql_user: str = Field(default="root", description="MySQL user")
    mysql_password: str = Field(default="", description="MySQL password")
    mysql_database: str = Field(default="zititex_db", description="MySQL database name")
    database_echo: bool = Field(
        default=False, description="Enable SQLAlchemy echo (SQL logging)"
    )

    # CORS settings
    allowed_origins: list[str] = Field(
        default=["*"], description="Allowed CORS origins"
    )
    allowed_methods: list[str] = Field(
        default=["*"], description="Allowed CORS methods"
    )
    allowed_headers: list[str] = Field(
        default=["*"], description="Allowed CORS headers"
    )

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
