"""
Test cases for service layer.

This module tests business logic services including
Mailgun email service integration.
"""

from unittest.mock import MagicMock, patch

import pytest
import requests

from app.services.mailgun import MailgunService


class TestMailgunService:
    """Test suite for MailgunService."""

    @pytest.fixture
    def mailgun_service(self):
        """Create a test MailgunService instance."""
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.mailgun_api_key = "test-api-key"
            mock_settings.mailgun_domain = "test.mailgun.org"
            mock_settings.mailgun_base_url = "https://api.mailgun.net/v3"
            service = MailgunService()
            return service

    @patch("app.services.mailgun.requests.post")
    def test_send_email_success(self, mock_post, mailgun_service):
        """Test successful email sending."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_email(
            to_emails=["test@example.com"],
            subject="Test Subject",
            text="Test message",
        )

        assert result is not None
        assert result["id"] == "test-message-id"
        mock_post.assert_called_once()

    @patch("app.services.mailgun.requests.post")
    def test_send_email_with_html(self, mock_post, mailgun_service):
        """Test sending email with HTML content."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_email(
            to_emails=["test@example.com"],
            subject="Test Subject",
            html="<h1>Test HTML</h1>",
        )

        assert result is not None
        call_args = mock_post.call_args
        assert "<h1>Test HTML</h1>" in str(call_args)

    @patch("app.services.mailgun.requests.post")
    def test_send_email_failure(self, mock_post, mailgun_service):
        """Test email sending failure."""
        mock_post.side_effect = requests.RequestException("Connection error")

        result = mailgun_service.send_email(
            to_emails=["test@example.com"],
            subject="Test Subject",
            text="Test message",
        )

        assert result is None

    def test_send_email_no_api_key(self):
        """Test email sending without API key."""
        with patch("app.core.config.settings") as mock_settings:
            mock_settings.mailgun_api_key = None
            mock_settings.mailgun_domain = None
            service = MailgunService()

            result = service.send_email(
                to_emails=["test@example.com"],
                subject="Test",
                text="Test",
            )

            assert result is None

    @patch("app.services.mailgun.requests.post")
    def test_send_contact_form_email_success(self, mock_post, mailgun_service):
        """Test successful contact form email sending."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_contact_form_email(
            full_name="Test User",
            email="user@example.com",
            phone="1234567890",
            message="Test message",
            admin_email="admin@test.com",
        )

        assert result is True
        # Should be called twice: once for admin, once for user
        assert mock_post.call_count == 2

    @patch("app.services.mailgun.requests.post")
    def test_send_contact_form_email_with_optional_fields(
        self, mock_post, mailgun_service
    ):
        """Test contact form email with optional fields."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_contact_form_email(
            full_name="Test User",
            email="user@example.com",
            phone="1234567890",
            message="Test message",
            admin_email="admin@test.com",
            company="Test Company",
            product_type="Textiles",
            quantity="Más de 10,000 unidades (opcional)",
        )

        assert result is True
        # Verify optional fields are in the email content
        call_args_str = str(mock_post.call_args_list)
        assert "Test Company" in call_args_str
        assert "Textiles" in call_args_str
        assert "Más de 10,000 unidades (opcional)" in call_args_str
        
    @patch("app.services.mailgun.requests.post")
    def test_send_contact_form_email_admin_fails(self, mock_post, mailgun_service):
        """Test contact form when admin email fails."""
        mock_post.side_effect = requests.RequestException("Connection error")

        result = mailgun_service.send_contact_form_email(
            full_name="Test User",
            email="user@example.com",
            phone="1234567890",
            message="Test message",
            admin_email="admin@test.com",
        )

        assert result is False

    @patch("app.services.mailgun.requests.post")
    def test_send_contact_form_email_user_confirmation_fails(
        self, mock_post, mailgun_service
    ):
        """Test contact form when user confirmation email fails."""
        # First call (admin email) succeeds
        admin_response = MagicMock()
        admin_response.status_code = 200
        admin_response.json.return_value = {"id": "admin-email-id"}
        
        # Second call (user email) fails
        user_response = MagicMock()
        user_response.status_code = 500
        user_response.json.return_value = {}
        
        mock_post.side_effect = [admin_response, user_response]

        result = mailgun_service.send_contact_form_email(
            full_name="Test User",
            email="user@example.com",
            phone="1234567890",
            message="Test message",
            admin_email="admin@test.com",
        )

        # Should still return True as admin email succeeded
        assert result is True

    @patch("app.services.mailgun.requests.post")
    def test_send_welcome_email(self, mock_post, mailgun_service):
        """Test welcome email sending."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_welcome_email(
            email="newuser@example.com", username="newuser"
        )

        assert result is True
        mock_post.assert_called_once()

    @patch("app.services.mailgun.requests.post")
    def test_send_template_email(self, mock_post, mailgun_service):
        """Test template email sending."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_template_email(
            to_emails=["test@example.com"],
            template_name="test-template",
            template_variables={"name": "Test User"},
        )

        assert result is not None
        call_args = mock_post.call_args
        assert "test-template" in str(call_args)

    @patch("app.services.mailgun.requests.post")
    def test_send_email_with_reply_to(self, mock_post, mailgun_service):
        """Test sending email with reply-to header."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_email(
            to_emails=["test@example.com"],
            subject="Test",
            text="Test",
            reply_to="reply@example.com",
        )

        assert result is not None
        call_args = mock_post.call_args
        call_data = call_args.kwargs.get("data", {})
        assert "h:Reply-To" in call_data
        assert call_data["h:Reply-To"] == "reply@example.com"

    @patch("app.services.mailgun.requests.post")
    def test_send_email_with_cc_bcc(self, mock_post, mailgun_service):
        """Test sending email with CC and BCC."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-message-id"}
        mock_post.return_value = mock_response

        result = mailgun_service.send_email(
            to_emails=["test@example.com"],
            subject="Test",
            text="Test",
            cc=["cc@example.com"],
            bcc=["bcc@example.com"],
        )

        assert result is not None
        call_args = mock_post.call_args
        call_data = call_args.kwargs.get("data", {})
        assert "cc" in call_data
        assert "bcc" in call_data

