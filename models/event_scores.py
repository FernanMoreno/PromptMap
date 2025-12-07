import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    JSON,
    String,
    Numeric,
    Text,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
class EventScore(Base):
    __tablename__ = "event_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )

    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)

    value_numeric: Mapped[Optional[float]] = mapped_column(Numeric(18, 6))

    value_text: Mapped[Optional[str]] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    event: Mapped["Event"] = relationship(back_populates="scores")