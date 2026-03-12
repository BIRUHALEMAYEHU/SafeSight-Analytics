from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.dependencies import get_current_active_user, require_role
from app.db.session import get_db
from app.models.rule import Rule as RuleModel
from app.models.user import User
from app.schemas import rule as rule_schema

router = APIRouter()


@router.get("/", response_model=List[rule_schema.Rule])
async def list_rules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """List all alert rules."""
    result = await db.execute(select(RuleModel))
    return result.scalars().all()


@router.post("/", response_model=rule_schema.Rule)
async def create_rule(
    rule_in: rule_schema.RuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Any:
    """
    Create a new alert rule. Admin only.

    Example rule:
    {
        "name": "Alert on unknown faces",
        "conditions": {"event_type": "unknown_face"},
        "action": {"alert_type": "intrusion", "priority": "critical"}
    }
    """
    rule = RuleModel(
        name=rule_in.name,
        conditions=rule_in.conditions,
        action=rule_in.action,
        is_active=rule_in.is_active,
    )
    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.put("/{rule_id}", response_model=rule_schema.Rule)
async def update_rule(
    rule_id: int,
    rule_in: rule_schema.RuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Any:
    """Update an alert rule. Admin only."""
    result = await db.execute(select(RuleModel).where(RuleModel.id == rule_id))
    rule = result.scalars().first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    update_data = rule_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)

    db.add(rule)
    await db.commit()
    await db.refresh(rule)
    return rule


@router.delete("/{rule_id}", response_model=rule_schema.Rule)
async def delete_rule(
    rule_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
) -> Any:
    """Delete an alert rule. Admin only."""
    result = await db.execute(select(RuleModel).where(RuleModel.id == rule_id))
    rule = result.scalars().first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    await db.delete(rule)
    await db.commit()
    return rule
