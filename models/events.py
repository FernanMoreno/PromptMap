import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    JSON,
    Integer,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )

    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
    )

    seq_index: Mapped[int] = mapped_column(Integer(), nullable=False)

    parent_event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("events.id", ondelete="SET NULL"),
        nullable=True,
    )

    prompt_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("prompts.id", ondelete="SET NULL")
    )

    prompt_version_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("prompt_versions.id", ondelete="SET NULL")
    )

    agent_name: Mapped[Optional[str]] = mapped_column(String(128))
    model_name: Mapped[Optional[str]] = mapped_column(String(128))
    role: Mapped[Optional[str]] = mapped_column(String(32))

    input_text: Mapped[Optional[str]] = mapped_column(Text())
    rendered_prompt: Mapped[Optional[str]] = mapped_column(Text())
    output_text: Mapped[Optional[str]] = mapped_column(Text())

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    finished_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )
    latency_ms: Mapped[Optional[int]] = mapped_column(Integer())
    tokens_in: Mapped[Optional[int]] = mapped_column(Integer())
    tokens_out: Mapped[Optional[int]] = mapped_column(Integer())
    cost: Mapped[Optional[float]] = mapped_column(Numeric(18, 6))

    status: Mapped[str] = mapped_column(
        String(32), default="completed", nullable=False
    )

    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    # -------------------- RELATIONSHIPS -------------------- #
    
    run: Mapped["Run"] = relationship(back_populates="events")

    prompt: Mapped[Optional["Prompt"]] = relationship(back_populates="events")

    prompt_version: Mapped[Optional["PromptVersion"]] = relationship(
        back_populates="events"
    )

    scores: Mapped[List["EventScore"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )

    parent: Mapped[Optional["Event"]] = relationship(
        "Event",
        remote_side="Event.id",
        back_populates="children",
    )

    children: Mapped[List["Event"]] = relationship(
        "Event",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
