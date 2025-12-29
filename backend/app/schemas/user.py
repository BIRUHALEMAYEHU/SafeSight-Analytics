from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    """Schema for creating a user"""
    username: str
    email: EmailStr
    password: str
    role: str = "viewer"


class UserUpdate(UserBase):
    """Schema for updating a user"""
    password: Optional[str] = None


class User(UserBase):
    """Schema for user response"""
    id: int
    
    class Config:
        from_attributes = True


class UserInDB(User):
    """User schema with hashed password"""
    hashed_password: str
