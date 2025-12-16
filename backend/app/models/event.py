from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from ..db.base import Base

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"))
    type: Mapped[str]  # person_detected, weapon_detected
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    event_metadata: Mapped[dict] = mapped_column("metadata", JSON) 
    snapshot_path: Mapped[str] # Path to image file
    
    # Relationships
    camera: Mapped["Camera"] = relationship(back_populates="events")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="event")
