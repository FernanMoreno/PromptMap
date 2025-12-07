import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PromptVersionParent(Base):
    __tablename__ = "prompt_version_parents"

    child_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    parent_version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    child: Mapped["PromptVersion"] = relationship(
        "PromptVersion",
        back_populates="parents",
        foreign_keys=[child_version_id],
    )

    parent: Mapped["PromptVersion"] = relationship(
        "PromptVersion",
        back_populates="children",
        foreign_keys=[parent_version_id],
    )
