from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column
from ..db.base import Base

class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    conditions: Mapped[dict] = mapped_column(JSON)
    action: Mapped[dict] = mapped_column(JSON)
    is_active: Mapped[bool] = mapped_column(default=True)
