import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class PromptBranch(Base):
    __tablename__ = "prompt_branches"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    prompt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prompts.id", ondelete="CASCADE"), 
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    head_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="SET NULL") 
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("prompt_id", "name", name = "uq_prompt_branches_prompt_name")
    )

    # Relationships

    prompt: Mapped["Prompt"] = relationship(back_populates="branches")

    head_version: Mapped[Optional["PromptVersion"]] = relationship(
        foreign_keys=[head_version_id],
        back_populates="branches_as_head",
        uselist=False
    )