# Implementation Plan - SafeSight Analytics

# Goal
Build a real-time intelligent video surveillance system that detects faces (Persons of Interest) and dangerous objects (Weapons) from live camera feeds and alerts security operators via a web dashboard.

## User Review Required
> [!IMPORTANT]
> **Architecture Decision**: The Vision Service will act as the "Eye". It will process video locally and send **Metadata/Alerts** to the Backend. For the Live Video Feed on the dashboard, the Vision Service will expose a lightweight MJPEG stream.

## Proposed Architecture

### 1. Vision Service (The "Eye")
- **Responsibility**: Capture video, run AI models, stream video, send alerts.
- **Tech**: Python, OpenCV, YOLOv8 (Objects), face_recognition (Faces).
- **Flow**:
    1.  Read Frame.
    2.  **Detect Objects**: Is there a weapon? -> If yes, send Alert to Backend.
    3.  **Detect Faces**: Is there a face? -> Encode -> Compare with Local Cache of "Wanted Persons". -> If match, send Alert to Backend.
    4.  **Annotate Frame**: Draw boxes/names on the frame.
    5.  **Stream**: Serve processed frame via HTTP (MJPEG) for the Frontend to display.

### 2. Backend Service (The "Brain")
- **Responsibility**: Manage data, handle alerts, communicate with Frontend.
- **Tech**: FastAPI, PostgreSQL (Database), WebSockets.
- **Flow**:
    -   **REST API**: Manage "Persons of Interest" (CRUD), Login/Auth, Retrieve Alert History.
    -   **WebSockets**: Push real-time alerts from Vision -> Backend -> Frontend.

### 3. Frontend (The "Dashboard")
- **Responsibility**: Display live insights and controls.
- **Tech**: React, Tailwind CSS.
- **Features**:
    -   **Live Monitor**: Grid view of camera feeds (connecting to Vision MJPEG stream).
    -   **Alert Feed**: Real-time sidebar showing "Weapon Detected" or "Person Identified: John Doe".
    -   **Management**: Admin panel to upload photos of "Banned/VIP" individuals.

---

## Development Phases

### Phase 1: Foundation & Database
- [ ] **Database**: Setup PostgreSQL (via Docker).
- [ ] **Schema**: Create tables for `Users`, `PersonsOfInterest` (Name, Photo, Status), `Alerts` (Type, Timestamp, Image).
- [ ] **Backend**: Create API endpoints to add/list "Persons of Interest".

### Phase 2: Vision Engine (The Core)
- [ ] **Object Detection**: Integrate YOLOv8 to detect 'person', 'knife', 'gun'.
- [ ] **Face Recognition**: Integrate `face_recognition` library.
    -   *Sync Mechanism*: Vision service needs to fetch known face encodings from Backend on startup/update.
- [ ] **Streaming**: Implement MJPEG streaming endpoint in Vision service.

### Phase 3: Real-time Integration
- [ ] **Communication**: Connect Vision to Backend (HTTP POST for alerts).
- [ ] **WebSockets**: specific WebSocket endpoint for Frontend to receive "Instant Alerts".
- [ ] **Frontend Dashboard**: Build the Live View and Alert Sidebar.

### Phase 4: Polish & Demo
- [ ] **Alert Logic**: Add "cooldown" to prevent spamming alerts for the same person every millisecond.
- [ ] **UI Polish**: Make it look "Premium" (Dark mode, glassmorphism).

## Verification Plan

### Automated Tests
- Backend: Test API endpoints (Create Person, Get Alerts).
- Vision: Unit test detection logic with static images.

### Manual Verification
- **End-to-End Demo**:
    1.  Upload a photo of myself as "Wanted".
    2.  Walk in front of the camera.
    3.  **Expectation**: Dashboard immediately flashes RED with my name and timestamp.
    4.  Hold a mock weapon (e.g., a banana or toy).
    5.  **Expectation**: Dashboard alerts "Weapon Detected".
