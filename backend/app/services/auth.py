"""
AUTHENTICATION SYSTEM (EDUCATIONAL DEMO)

Features:
- User registration
- Password hashing (bcrypt)
- Login + JWT access token
- Refresh tokens
- Role-based authorization
- Dependency-based auth guards
- In-memory "database" (replace with real DB in prod)

Run:
    pip install fastapi uvicorn python-jose passlib[bcrypt]

Start server:
    uvicorn auth_app:app --reload
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from uuid import uuid4

from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

SECRET_KEY = "SUPER_SECRET_CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

app = FastAPI(title="Auth Demo")

# -------------------------------------------------------------------
# FAKE DATABASE
# -------------------------------------------------------------------

users_db: Dict[str, dict] = {}
refresh_tokens_db: Dict[str, str] = {}

# -------------------------------------------------------------------
# MODELS
# -------------------------------------------------------------------

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    email: EmailStr
    is_active: bool
    role: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    role: str

# -------------------------------------------------------------------
# PASSWORD UTILITIES
# -------------------------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# -------------------------------------------------------------------
# TOKEN UTILITIES
# -------------------------------------------------------------------

def create_access_token(*, subject: str, role: str) -> str:
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "role": role,
        "exp": expires,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    token = str(uuid4())
    refresh_tokens_db[token] = user_id
    return token

# -------------------------------------------------------------------
# USER UTILITIES
# -------------------------------------------------------------------

def get_user_by_email(email: str):
    return users_db.get(email)

def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user

# -------------------------------------------------------------------
# DEPENDENCIES
# -------------------------------------------------------------------

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return User(
        id=user["id"],
        email=user["email"],
        is_active=user["is_active"],
        role=user["role"],
    )

def require_role(required_role: str):
    def checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user
    return checker

# -------------------------------------------------------------------
# AUTH ROUTES
# -------------------------------------------------------------------

@app.post("/auth/register", response_model=User)
def register_user(data: UserCreate):
    if data.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid4())

    users_db[data.email] = {
        "id": user_id,
        "email": data.email,
        "hashed_password": hash_password(data.password),
        "is_active": True,
        "role": "user",
        "created_at": datetime.utcnow(),
    }

    return User(
        id=user_id,
        email=data.email,
        is_active=True,
        role="user",
    )

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        subject=user["email"],
        role=user["role"],
    )
    refresh_token = create_refresh_token(user["id"])

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@app.post("/auth/refresh", response_model=Token)
def refresh_token(refresh_token: str):
    user_id = refresh_tokens_db.get(refresh_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = next(u for u in users_db.values() if u["id"] == user_id)

    access_token = create_access_token(
        subject=user["email"],
        role=user["role"],
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# -------------------------------------------------------------------
# PROTECTED ROUTES
# -------------------------------------------------------------------

@app.get("/me")
def get_profile(user: User = Depends(get_current_user)):
    return user

@app.get("/admin")
def admin_only(user: User = Depends(require_role("admin"))):
    return {"message": f"Welcome admin {user.email} 👑"}

# -------------------------------------------------------------------
# DEV SEED
# -------------------------------------------------------------------

def seed_admin():
    users_db["admin@example.com"] = {
        "id": "admin-1",
        "email": "admin@example.com",
        "hashed_password": hash_password("admin123"),
        "is_active": True,
        "role": "admin",
        "created_at": datetime.utcnow(),
    }

seed_admin()
