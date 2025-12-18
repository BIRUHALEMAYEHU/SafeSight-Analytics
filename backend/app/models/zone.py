from sqlalchemy import ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db.base import Base

class Zone(Base):
    __tablename__ = "zones"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    camera_id: Mapped[int] = mapped_column(ForeignKey("cameras.id"))
    name: Mapped[str]
    type: Mapped[str] = mapped_column(default="restricted")  # restricted, safe, monitoring
    polygon: Mapped[list] = mapped_column(JSON)  # List of [x, y] coordinates
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Relationships
    camera: Mapped["Camera"] = relationship(back_populates="zones")
