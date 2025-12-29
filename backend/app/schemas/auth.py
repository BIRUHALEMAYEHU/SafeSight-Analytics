from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Token response model"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Refresh token request"""
    refresh_token: str


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: str


class PasswordReset(BaseModel):
    """Password reset with token"""
    token: str
    new_password: str


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: Optional[str] = None
    type: Optional[str] = "access"


class UserLogin(BaseModel):
    """Login request"""
    username: str
    password: str


class UserRegister(BaseModel):
    """Registration request"""
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = "viewer"
