from typing import Optional, List
from pydantic import BaseModel

# Shared properties
class CameraBase(BaseModel):
    name: Optional[str] = None
    rtsp_url: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = True

# Properties to receive via API on creation
class CameraCreate(CameraBase):
    name: str
    rtsp_url: str
    location: str

# Properties to receive via API on update
class CameraUpdate(CameraBase):
    pass

# Properties to return to client
class Camera(CameraBase):
    id: int

    class Config:
        from_attributes = True
