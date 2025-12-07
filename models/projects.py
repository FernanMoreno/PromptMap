import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )

    description: Mapped[Optional[str]] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.utcnow
    )

    # Relationships
    runs: Mapped[List["Run"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    prompts: Mapped[List["Prompt"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )