"""
Services package.

This package contains business logic services that implement application
use cases and orchestrate interactions between repositories and external APIs.
"""

from app.services.mailgun import MailgunService, mailgun_service

__all__ = ["MailgunService", "mailgun_service"]

