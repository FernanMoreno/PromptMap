import uuid
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    JSON,
    Integer,
    Numeric,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    from_prompt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prompts.id", ondelete="CASCADE"),
        nullable=False,
    )

    to_prompt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("prompts.id", ondelete="CASCADE"),
        nullable=False,
    )

    from_prompt_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="SET NULL")
    )

    to_prompt_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="SET NULL")
    )

    transitions_count: Mapped[int] = mapped_column(
        Integer(), nullable=False, default=0
    )

    avg_latency_ms: Mapped[Optional[float]] = mapped_column(Numeric(18, 3))

    avg_cost: Mapped[Optional[float]] = mapped_column(Numeric(18, 6))
    
    avg_score: Mapped[Optional[float]] = mapped_column(Numeric(10, 4))

    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "from_prompt_id",
            "to_prompt_id",
            "from_prompt_version_id",
            "to_prompt_version_id",
            name="uq_edges_project_from_to_version",
        ),
    )

    # Relationships

    from_prompt: Mapped["Prompt"] = relationship(
        foreign_keys=[from_prompt_id]
    )

    to_prompt: Mapped["Prompt"] = relationship(
        foreign_keys=[to_prompt_id]
    )
