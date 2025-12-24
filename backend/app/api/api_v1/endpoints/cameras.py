from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.camera import Camera as CameraModel
from app.schemas import camera as camera_schema

router = APIRouter()

@router.get("/", response_model=List[camera_schema.Camera])
async def read_cameras(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve cameras.
    """
    result = await db.execute(select(CameraModel).offset(skip).limit(limit))
    cameras = result.scalars().all()
    return cameras

@router.post("/", response_model=camera_schema.Camera)
async def create_camera(
    camera_in: camera_schema.CameraCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create new camera.
    """
    # Check if camera with same name exists
    result = await db.execute(select(CameraModel).where(CameraModel.name == camera_in.name))
    existing_camera = result.scalars().first()
    if existing_camera:
        raise HTTPException(status_code=400, detail="Camera with this name already exists")
    
    camera = CameraModel(
        name=camera_in.name,
        rtsp_url=camera_in.rtsp_url,
        location=camera_in.location,
        is_active=camera_in.is_active
    )
    db.add(camera)
    await db.commit()
    await db.refresh(camera)
    return camera

@router.get("/{camera_id}", response_model=camera_schema.Camera)
async def read_camera(
    camera_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get camera by ID.
    """
    result = await db.execute(select(CameraModel).where(CameraModel.id == camera_id))
    camera = result.scalars().first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

@router.put("/{camera_id}", response_model=camera_schema.Camera)
async def update_camera(
    camera_id: int,
    camera_in: camera_schema.CameraUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update a camera.
    """
    result = await db.execute(select(CameraModel).where(CameraModel.id == camera_id))
    camera = result.scalars().first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    update_data = camera_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(camera, field, value)
    
    db.add(camera)
    await db.commit()
    await db.refresh(camera)
    return camera

@router.delete("/{camera_id}", response_model=camera_schema.Camera)
async def delete_camera(
    camera_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete a camera.
    """
    result = await db.execute(select(CameraModel).where(CameraModel.id == camera_id))
    camera = result.scalars().first()
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    await db.delete(camera)
    await db.commit()
    return camera
