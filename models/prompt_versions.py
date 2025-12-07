import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    JSON
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class PromptVersion(Base):
    __tablename__ = "prompt_versions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    prompt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False
    )

    version_label: Mapped[Optional[str]] = mapped_column(String(64))

    branch_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("prompt_branches.id", ondelete="SET NULL")
    )

    template_text: Mapped[str] = mapped_column(Text(), nullable=False)

    hash: Mapped[str] = mapped_column(String(64), nullable=False)

    commit_message: Mapped[Optional[str]] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    created_by: Mapped[Optional[str]] = mapped_column(String(255))

    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    __table_args__ = (
        UniqueConstraint("prompt_id", "hash", name="uq_prompt_versions_hash")
    )

    # Relationships

    prompt: Mapped["Prompt"] = relationship(back_populates="versions")

    branch: Mapped[Optional["PromptBranch"]] = relationship(
        back_populates="versions",
        foreign_keys=[branch_id]
    )

    parents: Mapped[List["PromptVersionParent"]] = relationship(
        back_populates="child",
        foreign_keys="PromptVersionParent.child_version_id",
        cascade="all, delete-orphan"
    )

    children: Mapped[List["PromptVersionParent"]] = relationship(
        back_populates="parent",
        foreign_keys="PromptVersionParent.parent_version_id",
        cascade="all, delete-orphan"
    )

    events: Mapped[List["Event"]] = relationship(
        back_populates="prompt_version"
    )

    branches_where_head: Mapped[List["PromptBranch"]] = relationship(
        back_populates="head_version",
        foreign_keys="[PromptBranch.head_version_id]",
    )