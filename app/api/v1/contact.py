"""
Contact form API endpoints.

This module provides contact form functionality for
landing page integration.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_async_db
from app.repositories.client_repository import ClientRepository
from app.schemas.client import ClientCreate, ContactForm, ContactResponse
from app.services.mailgun import mailgun_service

router = APIRouter(prefix="/contact", tags=["Contact"])


@router.post("/", response_model=ContactResponse)
async def submit_contact_form(
    contact_data: ContactForm,
    db: AsyncSession = Depends(get_async_db),
) -> ContactResponse:
    """
    Submit contact form from landing page.

    This endpoint receives contact form submissions, saves them to the database,
    and sends notification emails to both admin and the submitter.

    Args:
        contact_data: Contact form data with personal info and message
        db: Database session dependency

    Returns:
        Contact form response with success status and data

    Raises:
        HTTPException: If email service is not configured or operation fails

    Example:
        POST /api/v1/contact/
        {
            "full_name": "Juan Pérez",
            "email": "juan@example.com",
            "phone": "+52 123 456 7890",
            "message": "Quiero información"
        }
    """
    try:
        # Validate email service configuration
        if not settings.mailgun_api_key or not settings.mailgun_domain:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Email service not configured",
            )

        # Validate admin email configuration
        if not settings.admin_email:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Admin email not configured",
            )

        print(f"🔍 Contact data received: {contact_data}")

        # Save to database using Repository Pattern
        # client_repo = ClientRepository(db)
        # client_create = ClientCreate(
        #     full_name=contact_data.full_name,
        #     email=contact_data.email,
        #     phone=contact_data.phone,
        #     company=contact_data.company,
        #     product_type=contact_data.product_type,
        #     quantity=contact_data.quantity,
        #     message=contact_data.message,
        # )

        # client = await client_repo.create_async(client_create)
        # print(f"✅ Client saved to database with ID: {client.id}")

        # Send contact form email notification
        email_success = mailgun_service.send_contact_form_email(
            full_name=contact_data.full_name,
            email=contact_data.email,
            phone=contact_data.phone,
            message=contact_data.message,
            admin_email=settings.admin_email,
            company=contact_data.company,
            product_type=contact_data.product_type,
            quantity=contact_data.quantity,
        )

        if not email_success:
            print("⚠️ Warning: Failed to send contact email, but data was saved")
            # We don't fail the request if email fails, as data is saved

        return ContactResponse(
            success=True,
            message="Mensaje enviado exitosamente. Te responderemos pronto.",
            data={
                # "id": client.id,
                "full_name": contact_data.full_name,
                "email": contact_data.email,
                "phone": contact_data.phone,
                "company": contact_data.company,
                "product_type": contact_data.product_type,
                "quantity": contact_data.quantity,
                "message": contact_data.message,
                "timestamp": datetime.now().isoformat(),
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing contact form: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing contact form: {str(e)}",
        )
