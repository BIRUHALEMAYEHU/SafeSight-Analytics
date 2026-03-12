from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from datetime import datetime

from app.api.dependencies import get_current_active_user
from app.db.session import get_db
from app.models.event import Event as EventModel
from app.models.alert import Alert as AlertModel
from app.models.rule import Rule as RuleModel
from app.models.user import User
from app.schemas import event as event_schema
from app.services.alert_stream import alert_stream

router = APIRouter()


@router.get("/", response_model=event_schema.EventList)
async def list_events(
    skip: int = 0,
    limit: int = 50,
    camera_id: Optional[int] = Query(None, description="Filter by camera"),
    type: Optional[str] = Query(None, description="Filter by event type"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    List detection events with optional filters.
    """
    query = select(EventModel)

    if camera_id is not None:
        query = query.where(EventModel.camera_id == camera_id)
    if type is not None:
        query = query.where(EventModel.type == type)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results, newest first
    query = query.order_by(desc(EventModel.timestamp)).offset(skip).limit(limit)
    result = await db.execute(query)
    events = result.scalars().all()

    return event_schema.EventList(items=events, total=total)


@router.post("/", response_model=event_schema.Event)
async def create_event(
    event_in: event_schema.EventCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a detection event.
    Called by the vision service when a detection occurs.
    No auth required so the vision service can call it freely.
    """
    event = EventModel(
        camera_id=event_in.camera_id,
        type=event_in.type,
        event_metadata=event_in.event_metadata,
        snapshot_path=event_in.snapshot_path,
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)

    # Check rules and auto-create alerts
    await _check_rules_and_alert(db, event)

    return event


@router.get("/{event_id}", response_model=event_schema.Event)
async def get_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a single event by ID."""
    result = await db.execute(select(EventModel).where(EventModel.id == event_id))
    event = result.scalars().first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


async def _check_rules_and_alert(db: AsyncSession, event: EventModel) -> None:
    """
    Check all active rules against the new event.
    If a rule matches, create an Alert and broadcast it via WebSocket.
    """
    result = await db.execute(select(RuleModel).where(RuleModel.is_active == True))
    rules = result.scalars().all()

    for rule in rules:
        conditions = rule.conditions or {}
        # Simple matching: check if event_type matches
        event_type_condition = conditions.get("event_type")
        if event_type_condition and event_type_condition != event.type:
            continue

        # Rule matches — create alert
        action = rule.action or {}
        alert = AlertModel(
            event_id=event.id,
            type=action.get("alert_type", "detection"),
            priority=action.get("priority", "warning"),
            status="new",
        )
        db.add(alert)
        await db.commit()
        await db.refresh(alert)

        # Broadcast via WebSocket
        await alert_stream.broadcast("alert", {
            "alert_id": alert.id,
            "event_id": event.id,
            "type": alert.type,
            "priority": alert.priority,
            "event_type": event.type,
            "camera_id": event.camera_id,
            "metadata": event.event_metadata,
        })
