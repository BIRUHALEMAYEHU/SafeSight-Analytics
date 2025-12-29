# Dashboard Overview - Tactical Command Center

## What is the Dashboard?

The **Tactical Command Center** is a high-fidelity, interactive security monitoring dashboard designed for real-time situational awareness. It provides a comprehensive view of all camera feeds, system telemetry, and security events in a single unified interface.

## Dashboard Layout

### 1. **Left Sidebar** (Unified Sidebar)
- **Navigation Menu**
  - ⚡ Control Center (Main Dashboard)
  - 📹 Vision Nodes (Camera Management)
  - 🔍 Threat Database (Security Event Logs)

- **AI Daily Briefing**
  - Summary of last 24 hours
  - Critical alerts count
  - System efficiency status
  - Zone security status

- **Live Telemetry**
  - Buffer Saturation (real-time percentage)
  - CPU Temperature (real-time monitoring)
  - Network Ping (latency tracking)
  - Updates every 2 seconds from backend

- **Security Event Log**
  - Real-time security events
  - Color-coded by severity:
    - 🔴 Critical (red, pulsing)
    - 🟠 High (orange)
    - 🟡 Medium (yellow)
    - ⚪ Low (gray)
  - Updates every 5 seconds from backend

- **Profile Node**
  - Current user name
  - Clearance level (ADMIN)
  - Active session timer (HH:MM:SS)

### 2. **Main Content Area**

#### **Hero Feed** (Primary Monitoring Channel)
- Large, high-priority live camera feed
- Features:
  - **Scanning Line Overlay** - Animated scanning effect
  - **Real-time Timestamp** - Current time display
  - **Live Status Indicator** - Green pulsing dot when online
  - **Interactive Controls**:
    - 📸 Snapshot - Capture current frame
    - ⏺ Record - Start/stop recording with timer
    - 🔲 Fullscreen - Expand to full screen

#### **Vision Nodes Grid** (Camera Cards)
- Grid of individual camera feeds
- Each card shows:
  - **Camera Name** - Identifies the location
  - **Live Status** - Green "LIVE" or red "OFFLINE" indicator
  - **Video Stream** - MJPEG feed from backend
  - **Interactive Controls** (on hover):
    - 📸 Snapshot - Download current frame
    - ⏺ Record - Toggle recording with timer
    - 🤖 Analyze - AI-powered frame analysis
    - 🔲 Fullscreen - Expand card to full screen

## Key Features

### 1. **Real-time Video Streaming**
- MJPEG streams from backend (`http://localhost:5000/video_feed`)
- Supports multiple cameras via `camera_id` parameter
- Automatic error handling with "SIGNAL LOST" placeholder

### 2. **AI Analysis** (Backend Integration)
- Click "Analyze" button on any camera card
- Captures current frame and sends to backend API
- Backend processes with Gemini 3 Flash AI
- Returns structured analysis:
  - Detected objects (persons, vehicles, etc.)
  - Threat detection (weapons, anomalies)
  - Threat level assessment
  - JSON-formatted results

### 3. **Snapshot Capture**
- Client-side frame capture
- Downloads image as JPEG file
- Filename includes camera name and timestamp

### 4. **Recording Controls**
- UI-only recording state (actual recording handled by backend)
- Visual timer display (MM:SS format)
- Red blinking indicator when active

### 5. **Fullscreen Mode**
- Browser Fullscreen API integration
- Works on any camera card or hero feed
- Exit with ESC key or button

### 6. **Real-time Data Updates**
- **Telemetry**: Fetched from `/api/v1/telemetry` every 2 seconds
- **Security Events**: Fetched from `/api/v1/events` every 5 seconds
- Automatic error handling and fallback

## Visual Design

- **Color Scheme**:
  - Base: `slate-950` (deep dark background)
  - Primary Accent: `cyan-500` (navigation, highlights)
  - Secondary Accent: `indigo-500` (AI indicators)
  - Status Colors: Green (online), Red (offline/critical)

- **Typography**: JetBrains Mono font for all technical data
- **Effects**: Glassmorphism (blurred overlays) for depth
- **Animations**: Pulsing indicators, scanning overlay, smooth transitions

## Backend API Endpoints Used

1. **Video Stream**: `GET http://localhost:5000/video_feed?camera_id={id}`
2. **AI Analysis**: `POST http://localhost:5000/api/v1/analyze`
3. **Telemetry**: `GET http://localhost:5000/api/v1/telemetry`
4. **Security Events**: `GET http://localhost:5000/api/v1/events`

## Authentication

- Protected route (requires login)
- Redirects to `/login` if not authenticated
- Session managed by NextAuth.js
- Default credentials: `admin` / `admin123`

## Responsive Design

- Sidebar: Fixed 320px width
- Main content: Responsive grid (1-3 columns based on screen size)
- Mobile-friendly controls and layouts

