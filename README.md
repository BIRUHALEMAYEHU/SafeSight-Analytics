<<<<<<< HEAD
# SafeSight Analytics

SafeSight Analytics is an intelligent, real-time video surveillance system designed for public safety applications. The system connects to one or more CCTV/IP cameras (or webcams/phone cameras for demo purposes) and analyzes live video streams in real time to detect faces, recognize individuals against a database, identify high-risk objects, and generate automated alerts for security operators.

The system addresses critical challenges in modern security environments by automatically scanning faces in live video against databases of persons of interest (wanted, banned, or VIP individuals), detecting dangerous objects like weapons, and providing a centralized dashboard for monitoring alerts and events. This improves situational awareness and response speed for security teams in public safety centers, campus security, event management, and law enforcement operations.

## Project Structure

```
SafeSight/
├── backend/          # FastAPI REST API
├── frontend/         # React + TypeScript + Vite + Tailwind CSS dashboard
├── vision/           # Python service for camera handling and video processing
├── deploy/           # Docker configuration files
└── docs/             # Documentation files
```

## Development Setup

### Prerequisites

- Python 3.11+ (for backend and vision services)
- Node.js 18+ and npm (for frontend)
- Webcam or video source (for vision service)

### Backend

Navigate to the backend directory and install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Vision Service

Navigate to the vision directory and install dependencies:

```bash
cd vision
pip install -r requirements.txt
```

Run the vision service:

```bash
python main.py
```

The service will attempt to open your webcam (camera index 0) or a video file. Press Ctrl+C to stop.

### Frontend

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

**Note:** Make sure the backend is running before starting the frontend, as it will attempt to connect to the backend health endpoint.

## Docker Deployment

To run all services using Docker Compose:

```bash
cd deploy
docker-compose up
```

This will start all three services (backend, frontend, and vision) in containers.

## Current Status

This is a minimal starter implementation. The current version includes:

- ✅ Basic FastAPI backend with health check endpoint
- ✅ Vision service that can read frames from webcam/video
- ✅ React frontend with Tailwind CSS that displays backend status
- ✅ Docker configuration for all services

**Not yet implemented:**
- Face detection and recognition
- Object detection
- Alert generation
- Database integration
- Full dashboard UI

## License

[Add your license here]

=======
# SafeSight-Analytics
SafeSight analytics: Intelligent Object and Face Recognition System for Real-Time Surveillance and Public Safety Applications.
>>>>>>> c7e82cf9bad6b8fc8bd95b85df8833585ad3c159
