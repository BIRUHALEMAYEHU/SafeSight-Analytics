from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.api.dependencies import get_current_active_user, require_role
from app.db.session import get_db
from app.models.alert import Alert as AlertModel
from app.models.user import User
from app.schemas import alert as alert_schema

router = APIRouter()


@router.get("/", response_model=List[alert_schema.AlertOut])
async def list_alerts(
    skip: int = 0,
    limit: int = 50,
    status: Optional[str] = Query(None, description="Filter by status: new, acknowledged, resolved"),
    priority: Optional[str] = Query(None, description="Filter by priority: critical, warning, info"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List alerts with optional filters."""
    query = select(AlertModel)

    if status is not None:
        query = query.where(AlertModel.status == status)
    if priority is not None:
        query = query.where(AlertModel.priority == priority)

    query = query.order_by(desc(AlertModel.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{alert_id}", response_model=alert_schema.AlertOut)
async def get_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get a single alert by ID."""
    result = await db.execute(select(AlertModel).where(AlertModel.id == alert_id))
    alert = result.scalars().first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/{alert_id}/acknowledge", response_model=alert_schema.AlertOut)
async def acknowledge_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Mark an alert as acknowledged."""
    result = await db.execute(select(AlertModel).where(AlertModel.id == alert_id))
    alert = result.scalars().first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = "acknowledged"
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert


@router.put("/{alert_id}/resolve", response_model=alert_schema.AlertOut)
async def resolve_alert(
    alert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Mark an alert as resolved."""
    result = await db.execute(select(AlertModel).where(AlertModel.id == alert_id))
    alert = result.scalars().first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = "resolved"
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    return alert
