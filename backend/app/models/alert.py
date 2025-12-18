from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..db.base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    type: Mapped[str] # intrusion, wanted_person
    priority: Mapped[str] = mapped_column(default="warning") # critical, warning, info
    status: Mapped[str] = mapped_column(default="new") # new, acknowledged, resolved
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    event: Mapped["Event"] = relationship(back_populates="alerts")
