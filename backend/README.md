# Phase 1: Database Foundation

## Overview
This PR establishes the complete database foundation for SafeSight Analytics, including all core models, migrations, and Docker setup.

## What's Included

### Database Models (`backend/app/models/`)
- **User**: Authentication and RBAC
- **Camera**: Camera configuration and management
- **Zone**: Polygon-based restricted zones
- **PersonOfInterest**: Face recognition database
- **Event**: Raw detection events (high volume)
- **Alert**: Processed alerts with priorities
- **Rule**: Rules engine definitions

### Infrastructure
- PostgreSQL 15 with asyncpg driver
- Alembic migrations configured
- Docker Compose with health checks
- Auto-migration on startup

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
# - Frontend: http://localhost:5173
# - PostgreSQL: localhost:5432
```

### Verify Database
```bash
# Run verification script
docker compose exec backend python scripts/verify_db.py
```

## Database Schema

```
users
├── id (PK)
├── username (unique)
├── hashed_password
├── role
└── is_active

cameras
├── id (PK)
├── name (unique)
├── rtsp_url
└── is_active

zones
├── id (PK)
├── camera_id (FK → cameras)
├── name
├── type
└── polygon (JSON)

persons_of_interest
├── id (PK)
├── name
├── type (wanted/vip/banned/staff)
├── face_encoding (JSON)
└── photo_path

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
└── action (JSON)
```

## Next Steps (Phase 2)
- Camera Management API (CRUD)
- POI Management API (upload photos)
- Basic Rules Engine implementation

## Technical Decisions
- **PostgreSQL**: Robust for structured data
- **asyncpg**: High-performance async operations
- **SQLAlchemy 2.0**: Modern ORM with async support
- **JSON fields**: Flexible storage for polygons, encodings, rules
