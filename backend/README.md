# SafeSight Analytics - Backend

## Overview
SafeSight Analytics is a comprehensive video surveillance system with face recognition, zone monitoring, and real-time alerting capabilities.

## Current Status

### ✅ Phase 1: Database Foundation (Complete)
- PostgreSQL database with 7 core models
- Alembic migrations
- Docker Compose setup
- Comprehensive test suite

### ✅ Phase 2: Core Logic (In Progress)
- ✅ Camera Management API (CRUD)
- ✅ Person of Interest API (CRUD + Image Upload)
- ✅ **User Authentication System**
  - JWT-based authentication
  - Role-based access control (admin, operator, viewer)
  - Refresh tokens (7-day expiration)
  - Password reset flow
- ⏳ Basic Rules Engine (Planned)

## Features

### 🔐 Authentication & Authorization
- **User Registration**: Create new user accounts with roles
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**:
  - **Admin**: Full access (create, read, update, delete)
  - **Operator**: Can manage cameras and persons (create, read, update)
  - **Viewer**: Read-only access
- **Refresh Tokens**: Long-lived sessions (7 days)
- **Password Reset**: Secure password recovery flow

### 📷 Camera Management
- Register RTSP cameras
- Configure camera settings
- Monitor camera status
- **Protected**: Requires authentication

### 👤 Person of Interest Management
- Add persons with photos
- Categorize (wanted, VIP, banned, staff)
- Upload face photos
- **Protected**: Admin/Operator only

## API Endpoints

### Authentication
```
POST   /api/v1/auth/users                # Create user (admin only)
POST   /api/v1/auth/login                # Login (returns access + refresh token)
GET    /api/v1/auth/me                   # Get current user
POST   /api/v1/auth/refresh              # Refresh access token
POST   /api/v1/auth/password-reset/request   # Request password reset
POST   /api/v1/auth/password-reset/confirm   # Confirm password reset
```

> **Security Note**: User creation is restricted to admins only. This system is designed for private, controlled deployments where user accounts are managed centrally rather than allowing self-registration.

### Cameras (Protected)
```
GET    /api/v1/cameras/                  # List cameras (any authenticated user)
POST   /api/v1/cameras/                  # Create camera (admin/operator)
GET    /api/v1/cameras/{id}              # Get camera details
PUT    /api/v1/cameras/{id}              # Update camera (admin/operator)
DELETE /api/v1/cameras/{id}              # Delete camera (admin only)
```

### Persons of Interest (Protected)
```
GET    /api/v1/persons/                  # List persons (any authenticated user)
POST   /api/v1/persons/                  # Create person (admin/operator)
GET    /api/v1/persons/{id}              # Get person details
PUT    /api/v1/persons/{id}              # Update person (admin/operator)
DELETE /api/v1/persons/{id}              # Delete person (admin only)
POST   /api/v1/persons/{id}/photo        # Upload photo (admin/operator)
```

### Other Endpoints
```
GET    /video_feed?camera_id={id}        # Stream video from camera
GET    /                                 # API info
GET    /docs                             # Interactive API documentation
```

## Running Locally

### Prerequisites
- Docker and Docker Compose installed

### Setup
```bash
# Start all services
cd deploy
docker compose up --build

# Services will be available at:
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Frontend: http://localhost:5173
# - PostgreSQL: localhost:5432
```

### Environment Variables
Create `.env` file in project root:
```bash
# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-secret-key-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=postgresql+asyncpg://safesight:changeme@database:5432/safesight
```

### Quick Start Example
```bash
# Note: The first admin user must be created directly in the database or via a setup script
# For testing, you can use the database seeding script or create via SQL

# 1. Login with your admin credentials
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=admin&password=yourpassword"

# Response: {"access_token": "...", "refresh_token": "...", "token_type": "bearer"}

# 2. Create a new user (admin only)
curl -X POST "http://localhost:8000/api/v1/auth/users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "operator1",
    "email": "operator@example.com",
    "password": "securepass123",
    "role": "operator"
  }'

# 3. Use token to access protected endpoints
curl -X GET "http://localhost:8000/api/v1/cameras/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Database Schema

```
users
├── id (PK)
├── username (unique)
├── email (unique)
├── hashed_password
├── full_name
├── role (admin/operator/viewer)
└── is_active

cameras
├── id (PK)
├── name (unique)
├── rtsp_url
├── location
└── is_active

zones
├── id (PK)
├── camera_id (FK → cameras)
├── name
├── type (restricted/monitoring)
└── polygon (JSON)

persons_of_interest
├── id (PK)
├── name
├── type (wanted/vip/banned/staff)
├── photo_path
├── face_encoding (JSON)
└── created_at

events
├── id (PK)
├── camera_id (FK → cameras)
├── type
├── timestamp
└── metadata (JSON)

alerts
├── id (PK)
├── event_id (FK → events)
├── type
├── priority (critical/warning/info)
└── status (new/acknowledged/resolved)

rules
├── id (PK)
├── name
├── conditions (JSON)
├── action (JSON)
└── is_active
```

## Testing

Run the comprehensive test suite:
```bash
# All tests
docker compose exec backend pytest tests/ -v

# Authentication tests only
docker compose exec backend pytest tests/test_auth.py tests/test_token_refresh.py -v

# Model tests
docker compose exec backend pytest tests/test_models.py -v
```

**Current Test Coverage:**
- ✅ 9 authentication tests
- ✅ 7 refresh token & password reset tests
- ✅ Model tests for all 7 database models

## Technical Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL 15 with asyncpg
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt via passlib
- **Testing**: pytest with pytest-asyncio
- **Containerization**: Docker & Docker Compose

## Security Notes

1. **Always change** the default `SECRET_KEY` in production
2. **Refresh tokens** should be stored securely (httpOnly cookies recommended)
3. **Password reset tokens** expire after 60 minutes
4. **CORS** is configured for localhost - update for production
5. All sensitive endpoints are **protected** with JWT authentication

## Next Steps (Phase 3)
- Complete Rules Engine implementation
- Real-time event ingestion from Vision service
- WebSocket alerts
- Email notifications for password resets
- Token revocation/blacklist

## Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Update documentation
5. Submit pull request
