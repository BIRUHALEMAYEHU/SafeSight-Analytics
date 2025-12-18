from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from ..db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    email: Mapped[Optional[str]]
    full_name: Mapped[Optional[str]]
    role: Mapped[str] = mapped_column(default="operator")
    is_active: Mapped[bool] = mapped_column(default=True)
