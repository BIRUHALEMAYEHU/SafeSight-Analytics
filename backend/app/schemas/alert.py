from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class AlertOut(BaseModel):
    """Returned to clients."""
    id: int
    event_id: int
    type: str
    priority: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AlertUpdate(BaseModel):
    """For acknowledging or resolving alerts."""
    status: str  # acknowledged, resolved
