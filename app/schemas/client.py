"""
Client schemas for request/response validation.

This module contains Pydantic models for contact form requests,
responses, and client data validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class ContactForm(BaseModel):
    """
    Contact form request schema.

    This schema validates incoming contact form submissions from the landing page.
    """

    full_name: str = Field(
        ...,
        description="Full name of the contact person",
        min_length=2,
        max_length=100,
        examples=["Juan Pérez"],
    )
    email: EmailStr = Field(
        ..., description="Email address", examples=["juan.perez@example.com"]
    )
    phone: str = Field(
        ...,
        description="Phone number",
        min_length=10,
        max_length=20,
        examples=["+52 123 456 7890"],
    )
    company: Optional[str] = Field(
        None,
        description="Company name (optional)",
        max_length=255,
        examples=["Empresa S.A."],
    )
    product_type: Optional[str] = Field(
        None,
        description="Type of product interested in",
        max_length=100,
        examples=["Textiles"],
    )
    quantity: Optional[int] = Field(
        None, description="Quantity requested", ge=1, examples=[100]
    )
    message: str = Field(
        ...,
        description="Message content",
        min_length=10,
        max_length=2000,
        examples=["Me gustaría obtener más información sobre sus productos."],
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """
        Validate phone number format.

        Args:
            v: Phone number string

        Returns:
            Validated phone number

        Raises:
            ValueError: If phone format is invalid
        """
        # Remove common separators for validation
        cleaned = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not any(char.isdigit() for char in cleaned):
            raise ValueError("Phone number must contain digits")
        return v

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "full_name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "phone": "+52 123 456 7890",
                "company": "Empresa S.A.",
                "product_type": "Textiles",
                "quantity": 100,
                "message": "Me gustaría obtener más información sobre sus productos.",
            }
        }


class ContactResponse(BaseModel):
    """
    Contact form response schema.

    This schema defines the response structure after successful form submission.
    """

    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: dict = Field(default_factory=dict, description="Response data")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Mensaje enviado exitosamente. Te responderemos pronto.",
                "data": {
                    "name": "Juan Pérez",
                    "email": "juan.perez@example.com",
                    "timestamp": "2024-01-15T10:30:00",
                },
            }
        }


class ClientCreate(BaseModel):
    """
    Schema for creating a new client record.

    Used internally for database operations.
    """

    full_name: str
    email: EmailStr
    phone: str
    company: Optional[str] = None
    product_type: Optional[str] = None
    quantity: Optional[int] = None
    message: str


class ClientUpdate(BaseModel):
    """
    Schema for updating client information.

    All fields are optional for partial updates.
    """

    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    product_type: Optional[str] = None
    quantity: Optional[int] = None
    message: Optional[str] = None


class ClientResponse(BaseModel):
    """
    Schema for client database record response.

    Returns complete client information including timestamps.
    """

    id: int
    full_name: str
    email: str
    phone: str
    company: Optional[str] = None
    product_type: Optional[str] = None
    quantity: Optional[int] = None
    message: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "full_name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "phone": "+52 123 456 7890",
                "company": "Empresa S.A.",
                "product_type": "Textiles",
                "quantity": 100,
                "message": "Me gustaría obtener más información.",
                "created_at": "2024-01-15T10:30:00",
                "updated_at": "2024-01-15T10:30:00",
            }
        }

