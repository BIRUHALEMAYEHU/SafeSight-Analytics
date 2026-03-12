from typing import Optional, Any
from pydantic import BaseModel


class RuleCreate(BaseModel):
    """Create a new alert rule."""
    name: str
    conditions: dict[str, Any]  # e.g. {"event_type": "unknown_face"}
    action: dict[str, Any]  # e.g. {"alert_type": "intrusion", "priority": "critical"}
    is_active: bool = True


class RuleUpdate(BaseModel):
    """Update an existing rule."""
    name: Optional[str] = None
    conditions: Optional[dict[str, Any]] = None
    action: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


class Rule(BaseModel):
    """Returned to clients."""
    id: int
    name: str
    conditions: dict[str, Any]
    action: dict[str, Any]
    is_active: bool

    class Config:
        from_attributes = True
