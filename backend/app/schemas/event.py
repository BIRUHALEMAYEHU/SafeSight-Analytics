from typing import Optional, Any
from pydantic import BaseModel
from datetime import datetime


class EventCreate(BaseModel):
    """Sent by the vision service when a detection occurs."""
    camera_id: int
    type: str  # person_detected, unknown_face, weapon_detected
    event_metadata: dict[str, Any] = {}
    snapshot_path: Optional[str] = None


class Event(BaseModel):
    """Returned to clients."""
    id: int
    camera_id: int
    type: str
    timestamp: datetime
    event_metadata: dict[str, Any]
    snapshot_path: Optional[str] = None

    class Config:
        from_attributes = True


class EventList(BaseModel):
    """Paginated event list."""
    items: list[Event]
    total: int
