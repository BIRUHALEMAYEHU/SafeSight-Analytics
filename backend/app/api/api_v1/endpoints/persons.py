from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.db.session import get_db
from app.models.person import PersonOfInterest as PersonModel
from app.schemas import person as person_schema

router = APIRouter()

@router.get("/", response_model=List[person_schema.Person])
async def read_persons(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Retrieve persons of interest.
    """
    result = await db.execute(select(PersonModel).offset(skip).limit(limit))
    persons = result.scalars().all()
    return persons

@router.post("/", response_model=person_schema.Person)
async def create_person(
    person_in: person_schema.PersonCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create new person of interest.
    """
    person = PersonModel(
        name=person_in.name,
        type=person_in.type,
        notes=person_in.notes,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person

@router.get("/{person_id}", response_model=person_schema.Person)
async def read_person(
    person_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get person by ID.
    """
    result = await db.execute(select(PersonModel).where(PersonModel.id == person_id))
    person = result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.put("/{person_id}", response_model=person_schema.Person)
async def update_person(
    person_id: int,
    person_in: person_schema.PersonUpdate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update a person.
    """
    result = await db.execute(select(PersonModel).where(PersonModel.id == person_id))
    person = result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    update_data = person_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(person, field, value)
    
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person

@router.delete("/{person_id}", response_model=person_schema.Person)
async def delete_person(
    person_id: int,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete a person.
    """
    result = await db.execute(select(PersonModel).where(PersonModel.id == person_id))
    person = result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    await db.delete(person)
    await db.commit()
    return person

from fastapi import UploadFile, File
import shutil
import os

@router.post("/{person_id}/photo", response_model=person_schema.Person)
async def upload_photo(
    person_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Upload photo for a person.
    """
    result = await db.execute(select(PersonModel).where(PersonModel.id == person_id))
    person = result.scalars().first()
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    
    # Create directory if not exists
    upload_dir = "static/photos"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"person_{person_id}{file_extension}"
    file_path = f"{upload_dir}/{file_name}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Update person record
    person.photo_path = f"/static/photos/{file_name}"
    db.add(person)
    await db.commit()
    await db.refresh(person)
    return person
