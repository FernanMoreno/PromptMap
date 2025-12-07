import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    Integer,
    Float,
    JSON
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Run(Base):
    __tablename__ = "runs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False
    )

    name: Mapped[Optional[str]] = mapped_column(String(255))

    input_user: Mapped[Optional[str]] = mapped_column(Text())

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="completed")

    error_message: Mapped[Optional[str]] = mapped_column(Text())

    total_tokens_in: Mapped[Optional[int]] = mapped_column(Integer())

    total_tokens_out: Mapped[Optional[int]] = mapped_column(Integer())

    total_cost: Mapped[Optional[float]] = mapped_column(Float())

    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    # Relationships

    project: Mapped["Project"] = relationship(back_populates="runs")

    events: Mapped[List["Event"]] = relationship(
        back_populates="run", cascade="all, delete-orphan",
        order_by="Event.seq_index"
    )

    scores: Mapped[List["RunScore"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )