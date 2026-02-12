# SafeSight Analytics

SafeSight Analytics is an intelligent, real-time video surveillance platform for public safety and security operations. It connects to CCTV/IP cameras (or webcams for demos), analyzes live video, and surfaces actionable alerts to operators through a web dashboard.

This repository contains the full system: a FastAPI backend, a Next.js frontend, a vision service for AI inference, and a PostgreSQL database.

## Table of Contents

- [What SafeSight Analytics Does](#what-safesight-analytics-does)
- [Who It Helps](#who-it-helps)
- [Current Capabilities vs. Planned Features](#current-capabilities-vs-planned-features)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Quick Start (Docker Compose)](#quick-start-docker-compose)
- [Local Development (No Docker)](#local-development-no-docker)
- [Step-by-Step Usage Walkthrough](#step-by-step-usage-walkthrough)
- [API Overview](#api-overview)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [License](#license)

> **📹 Recording a Demo Video?** Check out [LOCAL_SETUP_GUIDE.md](LOCAL_SETUP_GUIDE.md) for a complete step-by-step guide to run the system locally and verify everything works!

## What SafeSight Analytics Does

SafeSight Analytics continuously analyzes live video streams and turns visual events into actionable security intelligence. The system is designed for multi-camera environments where human operators can’t reliably monitor every feed simultaneously.

Core ideas:

- **Face detection and recognition**: Detects faces in video, compares them against a stored database of persons of interest (e.g., wanted, VIP, staff).
- **Object detection (planned / in-progress)**: Designed to identify restricted or high-risk objects (e.g., weapons). The vision service already includes ML dependencies for future detectors.
- **Rule-based alerting (planned / in-progress)**: Designed to combine detections with policies such as “weapon detected in a restricted zone.”
- **Operational dashboard**: Provides operators a centralized view of cameras, alerts, and event history.

## Who It Helps

SafeSight Analytics is built for security teams that need rapid situational awareness:

- **Public safety & law enforcement**: City surveillance centers, transit hubs, or urban monitoring.
- **Campus and enterprise security**: Universities, hospitals, offices, factories.
- **Event security**: Stadiums, festivals, and temporary command centers with many feeds.

## Current Capabilities vs. Planned Features

**Available today (in this repo):**

- FastAPI backend with authentication, role-based access, camera management, and persons of interest.
- PostgreSQL database models, migrations, and tests.
- Vision service with face detection and recognition via DeepFace.
- Video streaming endpoint for camera feeds.
- Next.js dashboard scaffolding and authentication setup.

**Planned / in-progress:**

- Object detection for high-risk items.
- Rules engine for multi-signal alerts.
- Real-time alert streaming to the dashboard via WebSockets.

## System Architecture

SafeSight Analytics is composed of four services:

1. **Frontend (Next.js)**
	- Operator dashboard.
	- Authentication flow (NextAuth).

2. **Backend (FastAPI)**
	- REST API for cameras, users, and persons of interest.
	- JWT-based authentication with role-based access control.
	- Video streaming endpoint.
	- Storage of uploaded face images and metadata.

3. **Vision Service (FastAPI)**
	- Ingests images or frames for analysis.
	- Detects faces and recognizes known persons.
	- Pulls persons of interest from the backend and caches locally.

4. **PostgreSQL Database**
	- Stores users, cameras, persons, zones, events, alerts, and rules.

### Data Flow (End-to-End)

1. Operator registers cameras and persons of interest via the backend API.
2. The vision service pulls the persons list and maintains a local cache for fast recognition.
3. The vision service analyzes frames and produces detection results.
4. The backend records events (and will generate alerts as the rules engine matures).
5. The dashboard displays live feeds, detections, and alerts.

## Repository Structure

```
backend/        FastAPI backend, database models, migrations, tests
frontend/       Next.js operator dashboard
vision/         AI vision service (face detection + recognition)
deploy/         Dockerfiles and docker-compose
docs/           Architecture and implementation notes
```

## Quick Start (Docker Compose)

### Prerequisites

- Docker
- Docker Compose

### Run the Full System

```bash
cd deploy
docker compose up --build
```

### Service URLs

- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- Frontend dashboard: http://localhost:5173
- Postgres: localhost:5432 (user: `safesight`, password: `changeme`, db: `safesight`)

> Note: Next.js typically runs on port 3000. This compose file exposes 5173 to keep ports consistent with prior Vite setups. If you run the frontend outside Docker, use http://localhost:3000.

## Local Development (No Docker)

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `backend/.env` file:

```env
SECRET_KEY=your-secret-key-minimum-32-characters
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_RESET_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=postgresql+asyncpg://safesight:changeme@localhost:5432/safesight
```

Run migrations and start the API:

```bash
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

Optional NextAuth setup: see `frontend/ENV_SETUP.md`.

### 3) Vision Service

```bash
cd vision
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export BACKEND_URL=http://localhost:8000
python main.py
```

> Camera access may require OS-level permissions. If running in Docker and using a local webcam, pass the device (e.g., `/dev/video0`) into the container.

## Step-by-Step Usage Walkthrough

1. **Start all services** (Docker Compose or local).
2. **Create an admin user** in the database (initial bootstrap):
	- There is no self-registration endpoint by design; admin accounts are created out-of-band.
	- Use a DB client to insert an admin user (with a bcrypt-hashed password). See backend tests or your preferred admin bootstrap method.
3. **Login** via `POST /api/v1/auth/login` to obtain JWT access/refresh tokens.
4. **Register cameras** via `POST /api/v1/cameras`.
5. **Add persons of interest** via `POST /api/v1/persons` and upload photos with `POST /api/v1/persons/{id}/photo`.
6. **Reload persons in vision service** using `POST /reload-persons` to refresh recognition cache.
7. **View live streams** using `GET /video_feed?camera_id={id}` or from the dashboard.

## API Overview

### Authentication

- `POST /api/v1/auth/users` (admin-only user creation)
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/password-reset/request`
- `POST /api/v1/auth/password-reset/confirm`

### Cameras

- `GET /api/v1/cameras`
- `POST /api/v1/cameras`
- `GET /api/v1/cameras/{id}`
- `PUT /api/v1/cameras/{id}`
- `DELETE /api/v1/cameras/{id}`

### Persons of Interest

- `GET /api/v1/persons`
- `POST /api/v1/persons`
- `GET /api/v1/persons/{id}`
- `PUT /api/v1/persons/{id}`
- `DELETE /api/v1/persons/{id}`
- `POST /api/v1/persons/{id}/photo`

### Vision Service

- `GET /` (health summary)
- `GET /health`
- `POST /analyze` (face detection + recognition)
- `POST /detect-only` (face detection only)
- `POST /reload-persons`

## Testing

Run tests inside Docker:

```bash
cd deploy
docker compose exec backend pytest -v
```

Or run locally:

```bash
cd backend
pytest -v
```

## Troubleshooting

- **Camera stream not visible**: Ensure the camera is reachable and the RTSP URL is valid. For webcam devices, confirm OS permissions and correct device index.
- **Vision service returns 0 known persons**: Add persons in the backend and call `POST /reload-persons` on the vision service.
- **Auth errors**: Ensure the admin user exists and the password is correctly hashed.
- **Frontend can’t reach API**: Confirm API URL and CORS allowlist. The backend allows `http://localhost:5173` and `http://localhost:3000` by default.

## Roadmap

- Object detection for restricted items (weapons, hazards)
- Rule engine for multi-signal alerts
- Real-time alert streaming (WebSockets)
- Advanced analytics and reporting

## License

This project is licensed under the MIT License. See `LICENSE` for details.
