import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Prompt(Base):
    __tablename__ = "prompts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), 
        nullable=False
    )

    key: Mapped[str] = mapped_column(String(255), nullable=False)
    
    description: Mapped[Optional[str]] = mapped_column(Text())

    default_branch: Mapped[str] = mapped_column(String(255), default="main",nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("project_id", "key", name="uq_prompt_project_key")
    )

    # Relationships

    project: Mapped["Project"] = relationship(back_populates="prompts")

    branches: Mapped[List["PromptBranch"]] = relationship(
        back_populates="prompt", cascade="all, delete-orphan"
    )

    versions: Mapped[List["PromptVersion"]] = relationship(
        back_populates="prompt", cascade="all, delete-orphan"
    )

    events: Mapped[List["PromptEvent"]] = relationship(
        back_populates="prompt"
    )