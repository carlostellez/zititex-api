"""
Client database model.

This module contains the SQLAlchemy model for the client table,
which stores contact form submissions.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Client(Base):
    """
    Client model for storing contact form submissions.

    This table stores all information submitted through the contact form,
    including personal details and message content.

    Attributes:
        id: Primary key, auto-incrementing integer
        full_name: Client's full name
        email: Client's email address
        phone: Client's phone number
        company: Client's company name (optional)
        product_type: Type of product interested in (optional)
        quantity: Quantity requested (optional)
        message: Client's message or inquiry
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """

    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    company = Column(String(255), nullable=True)
    product_type = Column(String(100), nullable=True)
    quantity = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        """String representation of Client model."""
        return f"<Client(id={self.id}, name='{self.full_name}', email='{self.email}')>"

    def to_dict(self) -> dict:
        """
        Convert model instance to dictionary.

        Returns:
            Dictionary representation of the client
        """
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "product_type": self.product_type,
            "quantity": self.quantity,
            "message": self.message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

