from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..db.base import Base

class Camera(Base):
    __tablename__ = "cameras"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    rtsp_url: Mapped[str]
    location: Mapped[str] = mapped_column(default="Unknown")
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Relationships
    zones: Mapped[List["Zone"]] = relationship(back_populates="camera", cascade="all, delete-orphan")
    events: Mapped[List["Event"]] = relationship(back_populates="camera")
