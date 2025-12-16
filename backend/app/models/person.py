from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON
from typing import Optional
from ..db.base import Base

class PersonOfInterest(Base):
    __tablename__ = "persons_of_interest"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(index=True)
    type: Mapped[str] = mapped_column(default="wanted")  # wanted, vip, banned, staff
    photo_path: Mapped[Optional[str]]
    face_encoding: Mapped[Optional[list]] = mapped_column(JSON)  # 128-d vector
    notes: Mapped[Optional[str]]
    created_at: Mapped[str] # keeping simple for now, should be datetime
