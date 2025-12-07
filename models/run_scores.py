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
class RunScore(Base):
    __tablename__ = "run_scores"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )

    run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("runs.id", ondelete="CASCADE"),
        nullable=False,
    )

    metric_name: Mapped[str] = mapped_column(String(128), nullable=False)

    value_numeric: Mapped[Optional[float]] = mapped_column(Numeric(18, 6))

    value_text: Mapped[Optional[str]] = mapped_column(Text())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow
    )
    
    metadata: Mapped[Optional[dict]] = mapped_column(JSON)

    run: Mapped["Run"] = relationship(back_populates="scores")