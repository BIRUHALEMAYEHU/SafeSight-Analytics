from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

# Shared properties
class PersonBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    notes: Optional[str] = None

# Properties to receive via API on creation
class PersonCreate(PersonBase):
    name: str
    type: str

# Properties to receive via API on update
class PersonUpdate(PersonBase):
    pass

# Properties to return to client
class Person(PersonBase):
    id: int
    photo_path: Optional[str] = None
    photo_mime: Optional[str] = None
    photo_size: Optional[int] = None
    photo_checksum: Optional[str] = None
    photo_uploaded_at: Optional[datetime] = None
    face_encoding: Optional[List[float]] = None
    created_at: str 

    class Config:
        from_attributes = True
