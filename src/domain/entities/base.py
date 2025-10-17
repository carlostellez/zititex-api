"""Base entity class."""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """Base entity with common fields."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

