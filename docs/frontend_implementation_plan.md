# Frontend Implementation Plan - SafeSight Analytics Dashboard

## 🎯 Overall Vision

Build a modern, real-time command and control dashboard for security operators to monitor multiple camera feeds, manage persons of interest, and respond to AI-generated alerts.

### Final Product Features
- **Live Monitoring**: Multi-camera grid with real-time video streams
- **Alert Management**: Prioritized alert feed with filtering and acknowledgment
- **Person Registry**: Upload and manage persons of interest (WANTED/VIP/BANNED)
- **Camera Configuration**: Add, edit, and monitor camera sources
- **Analytics Dashboard**: Statistics and trends (Phase 4)
- **Zone Management**: Draw restricted areas on camera feeds (Phase 3)

---

## 🖼️ Visual Overview

### Dashboard Layout (Final State)
```
┌─────────────────────────────────────────────────────────────────────┐
│  SafeSight Analytics                    [User] [Settings] [Logout]  │
├─────────────────────────────────────────────────────────────────────┤
│ [Dashboard] [Cameras] [Persons] [Alerts] [Zones] [Analytics]        │
├──────────────────────────────────────┬──────────────────────────────┤
│                                      │  🔴 CRITICAL ALERTS          │
│  ┌────────────┐  ┌────────────┐     │  ┌─────────────────────────┐ │
│  │ Camera 1   │  │ Camera 2   │     │  │ ⚠️ Weapon Detected      │ │
│  │ [VIDEO]    │  │ [VIDEO]    │     │  │ Camera: Front Entrance  │ │
│  │ Front Door │  │ Parking    │     │  │ 2 mins ago             │ │
│  └────────────┘  └────────────┘     │  └─────────────────────────┘ │
│                                      │  ┌─────────────────────────┐ │
│  ┌────────────┐  ┌────────────┐     │  │ 👤 Person Identified    │ │
│  │ Camera 3   │  │ Camera 4   │     │  │ Name: John Doe (WANTED) │ │
│  │ [VIDEO]    │  │ [VIDEO]    │     │  │ Camera: Lobby          │ │
│  │ Lobby      │  │ Back Exit  │     │  │ 5 mins ago             │ │
│  └────────────┘  └────────────┘     │  └─────────────────────────┘ │
│                                      │                              │
│  📊 System Status:                   │  ⚠️ WARNING ALERTS           │
│  • 4 Cameras Active                  │  ┌─────────────────────────┐ │
│  • 12 Persons Monitored              │  │ 🚶 Zone Intrusion       │ │
│  • 2 Active Alerts                   │  │ Camera: Server Room     │ │
│                                      │  │ 15 mins ago            │ │
│                                      │  └─────────────────────────┘ │
└──────────────────────────────────────┴──────────────────────────────┘
```

### Component Hierarchy
```
App
├── Layout
│   ├── Navbar
│   │   ├── Logo
│   │   ├── Navigation Links
│   │   └── User Menu
│   └── Main Content Area
│       └── [Page Content]
│
├── Pages
│   ├── Dashboard
│   │   ├── VideoGrid
│   │   │   └── VideoPlayer (x4)
│   │   ├── AlertFeed
│   │   │   └── AlertCard (xN)
│   │   └── SystemStats
│   │
│   ├── Cameras
│   │   ├── CameraList
│   │   │   └── CameraCard (xN)
│   │   └── AddCameraForm
│   │
│   ├── Persons
│   │   ├── PersonGrid
│   │   │   └── PersonCard (xN)
│   │   └── AddPersonForm
│   │
│   └── Alerts
│       ├── AlertTable
│       ├── FilterBar
│       └── AlertDetailModal
│
└── Shared Components
    ├── Button
    ├── Input
    ├── Modal
    ├── Badge
    └── Card
```

---

## 📅 Development Phases

### Phase 1: Foundation & Core Layout (Week 1)
**Goal**: Set up project structure, design system, and navigation

#### Deliverables
- ✅ Next.js project structure
- ✅ Tailwind CSS configured
- ✅ Design tokens (colors, spacing, typography)
- ✅ Layout component with navbar
- ✅ Routing between pages
- ✅ Shared UI components (Button, Card, Badge, Input)

#### Tasks
1. **Setup Design System** (`app/globals.css`)
   ```css
   /* Color Palette */
   --color-primary: #3B82F6;      /* Blue */
   --color-danger: #EF4444;       /* Red for critical alerts */
   --color-warning: #F59E0B;      /* Orange for warnings */
   --color-success: #10B981;      /* Green for active status */
   --color-dark: #1F2937;         /* Dark background */
   --color-light: #F9FAFB;        /* Light background */
   ```

2. **Create Layout** (`app/layout.tsx`)
   - Top navbar with logo and navigation
   - Sidebar (optional, for future)
   - Footer with system info

3. **Build Shared Components** (`components/ui/`)
   - `Button.tsx` (primary, secondary, danger variants)
   - `Card.tsx` (container for content)
   - `Badge.tsx` (status indicators: ACTIVE, CRITICAL, WARNING)
   - `Input.tsx` (text input with validation styling)
   - `Modal.tsx` (popup for forms/details)

4. **Create Page Stubs** (Empty pages with titles)
   - `app/dashboard/page.tsx`
   - `app/cameras/page.tsx`
   - `app/persons/page.tsx`
   - `app/alerts/page.tsx`

#### Visual Example: Navbar Component
```
┌─────────────────────────────────────────────────────────────┐
│ 🛡️ SafeSight  [Dashboard] [Cameras] [Persons] [Alerts]  👤 │
└─────────────────────────────────────────────────────────────┘
```

#### Acceptance Criteria
- [ ] Can navigate between all pages
- [ ] Navbar highlights active page
- [ ] All shared components render correctly
- [ ] Design is responsive (mobile, tablet, desktop)
- [ ] Dark mode theme applied

---

### Phase 2: Camera Management (Week 1-2)
**Goal**: Build UI for managing camera sources

#### Deliverables
- Camera list page with grid layout
- Add/Edit camera form
- Camera status indicators
- Mock data for cameras

#### Tasks
1. **Create Camera Card Component** (`components/CameraCard.tsx`)
   ```
   ┌─────────────────────────┐
   │  📹 Front Entrance      │
   │  Location: Building A   │
   │  Status: 🟢 Active      │
   │  [Edit] [Delete]        │
   └─────────────────────────┘
   ```

2. **Build Camera List Page** (`app/cameras/page.tsx`)
   - Grid layout (3 columns on desktop)
   - Search/filter bar
   - "Add Camera" button

3. **Create Add/Edit Camera Form** (`components/CameraForm.tsx`)
   - Fields: Name, RTSP URL, Location
   - Validation (required fields)
   - Cancel/Save buttons

4. **Add Mock Data**
   ```typescript
   const mockCameras = [
     { id: 1, name: 'Front Entrance', rtsp_url: 'rtsp://...', location: 'Building A', is_active: true },
     { id: 2, name: 'Parking Lot', rtsp_url: 'rtsp://...', location: 'Building B', is_active: false },
     { id: 3, name: 'Lobby', rtsp_url: 'rtsp://...', location: 'Main Building', is_active: true },
   ];
   ```

5. **Mark API Integration Points**
   ```typescript
   // TODO: API - Replace with actual fetch
   // const response = await fetch('http://localhost:8000/api/v1/cameras');
   // const cameras = await response.json();
   ```

#### Visual Example: Camera Management Page
```
┌─────────────────────────────────────────────────────────────┐
│  Cameras                                    [+ Add Camera]   │
├─────────────────────────────────────────────────────────────┤
│  [Search cameras...]                        [Filter ▼]      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ 📹 Front     │  │ 📹 Parking   │  │ 📹 Lobby     │      │
│  │ Building A   │  │ Building B   │  │ Main Bldg    │      │
│  │ 🟢 Active    │  │ 🔴 Inactive  │  │ 🟢 Active    │      │
│  │ [Edit] [Del] │  │ [Edit] [Del] │  │ [Edit] [Del] │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

#### Acceptance Criteria
- [ ] Camera cards display all information
- [ ] Add camera form opens in modal
- [ ] Form validation works (required fields)
- [ ] Edit/Delete buttons are visible
- [ ] Grid is responsive

---

### Phase 3: Persons of Interest (Week 2)
**Goal**: Build UI for managing person registry

#### Deliverables
- Person card grid with photos
- Upload person form
- Type badges (WANTED, VIP, BANNED)
- Filter by person type

#### Tasks
1. **Create Person Card Component** (`components/PersonCard.tsx`)
   ```
   ┌─────────────────────────┐
   │  [Photo Placeholder]    │
   │  John Doe               │
   │  🔴 WANTED              │
   │  Added: 2024-01-15      │
   │  [View] [Delete]        │
   └─────────────────────────┘
   ```

2. **Build Person List Page** (`app/persons/page.tsx`)
   - Grid layout (4 columns)
   - Filter by type (All, WANTED, VIP, BANNED)
   - "Add Person" button

3. **Create Add Person Form** (`components/PersonForm.tsx`)
   - Fields: Name, Photo Upload, Type (dropdown), Notes
   - Photo preview before upload
   - Validation

4. **Add Mock Data**
   ```typescript
   const mockPersons = [
     { id: 1, name: 'John Doe', type: 'WANTED', photo_path: '/mock/john.jpg', notes: 'Suspect in robbery' },
     { id: 2, name: 'Jane Smith', type: 'VIP', photo_path: '/mock/jane.jpg', notes: 'CEO' },
     { id: 3, name: 'Bob Johnson', type: 'BANNED', photo_path: '/mock/bob.jpg', notes: 'Trespasser' },
   ];
   ```

5. **Implement Photo Upload UI** (File input with preview)
   ```typescript
   // TODO: API - Upload to backend
   // const formData = new FormData();
   // formData.append('photo', file);
   // await fetch('http://localhost:8000/api/v1/persons', { method: 'POST', body: formData });
   ```

#### Visual Example: Persons Page
```
┌─────────────────────────────────────────────────────────────┐
│  Persons of Interest                     [+ Add Person]      │
├─────────────────────────────────────────────────────────────┤
│  [All] [WANTED] [VIP] [BANNED]                              │
├─────────────────────────────────────────────────────────────┤
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │
│  │ [IMG]  │  │ [IMG]  │  │ [IMG]  │  │ [IMG]  │            │
│  │ John   │  │ Jane   │  │ Bob    │  │ Alice  │            │
│  │🔴WANTED│  │🟢VIP   │  │🟠BANNED│  │🔴WANTED│            │
│  │ [View] │  │ [View] │  │ [View] │  │ [View] │            │
│  └────────┘  └────────┘  └────────┘  └────────┘            │
└─────────────────────────────────────────────────────────────┘
```

#### Acceptance Criteria
- [ ] Person cards show photo (or placeholder)
- [ ] Type badges have correct colors
- [ ] Filter buttons work (show/hide by type)
- [ ] Photo upload preview works
- [ ] Form validation works

---

### Phase 4: Live Dashboard (Week 2-3)
**Goal**: Build the main monitoring interface

#### Deliverables
- Video grid (4 cameras)
- Alert feed sidebar
- System statistics
- Mock video streams

#### Tasks
1. **Create Video Player Component** (`components/VideoPlayer.tsx`)
   ```
   ┌─────────────────────────┐
   │  [VIDEO STREAM]         │
   │                         │
   │  Front Entrance         │
   │  🟢 Live                │
   └─────────────────────────┘
   ```

2. **Build Video Grid** (`app/dashboard/page.tsx`)
   - 2x2 grid layout
   - Each cell shows VideoPlayer
   - Fullscreen button for each video

3. **Create Alert Card Component** (`components/AlertCard.tsx`)
   ```
   ┌─────────────────────────────┐
   │ ⚠️ Weapon Detected          │
   │ Camera: Front Entrance      │
   │ Confidence: 95%             │
   │ 2 minutes ago               │
   │ [View Details] [Acknowledge]│
   └─────────────────────────────┘
   ```

4. **Build Alert Feed Sidebar** (`components/AlertFeed.tsx`)
   - Scrollable list of alerts
   - Color-coded by severity (red=critical, orange=warning)
   - Auto-scroll to newest

5. **Add System Stats Widget** (`components/SystemStats.tsx`)
   ```
   ┌─────────────────────────┐
   │ 📊 System Status        │
   │ • 4 Cameras Active      │
   │ • 12 Persons Monitored  │
   │ • 2 Active Alerts       │
   │ • Uptime: 24h 15m       │
   └─────────────────────────┘
   ```

6. **Mock Video Stream** (Use placeholder or test pattern)
   ```typescript
   // TODO: API - Connect to real video feed
   // <img src="http://localhost:8000/video_feed" />
   
   // For now, use placeholder
   <img src="/placeholder-video.jpg" alt="Camera feed" />
   ```

7. **Mock Alert Data**
   ```typescript
   const mockAlerts = [
     { id: 1, type: 'WEAPON_DETECTED', severity: 'CRITICAL', camera: 'Front Entrance', timestamp: '2 mins ago' },
     { id: 2, type: 'PERSON_IDENTIFIED', severity: 'WARNING', camera: 'Lobby', person: 'John Doe', timestamp: '5 mins ago' },
   ];
   ```

#### Visual Example: Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  Live Monitoring                                            │
├──────────────────────────────────┬──────────────────────────┤
│  ┌──────────┐  ┌──────────┐     │  🔴 ALERTS (2)           │
│  │ [VIDEO]  │  │ [VIDEO]  │     │  ┌────────────────────┐  │
│  │ Front    │  │ Parking  │     │  │ ⚠️ Weapon Detected │  │
│  │ 🟢 Live  │  │ 🟢 Live  │     │  │ Front Entrance     │  │
│  └──────────┘  └──────────┘     │  │ 2 mins ago        │  │
│                                  │  └────────────────────┘  │
│  ┌──────────┐  ┌──────────┐     │  ┌────────────────────┐  │
│  │ [VIDEO]  │  │ [VIDEO]  │     │  │ 👤 John Doe       │  │
│  │ Lobby    │  │ Back     │     │  │ Lobby             │  │
│  │ 🟢 Live  │  │ 🟢 Live  │     │  │ 5 mins ago        │  │
│  └──────────┘  └──────────┘     │  └────────────────────┘  │
│                                  │                          │
│  📊 System Status                │  [View All Alerts →]     │
│  • 4 Cameras Active              │                          │
│  • 12 Persons Monitored          │                          │
└──────────────────────────────────┴──────────────────────────┘
```

#### Acceptance Criteria
- [ ] 4 video players render in grid
- [ ] Alert feed shows mock alerts
- [ ] Alerts are color-coded by severity
- [ ] System stats display correctly
- [ ] Layout is responsive

---

### Phase 5: Alert History (Week 3)
**Goal**: Build searchable alert archive

#### Deliverables
- Alert table with sorting
- Filter by date, type, severity
- Alert detail modal
- Export button (UI only)

#### Tasks
1. **Create Alert Table Component** (`components/AlertTable.tsx`)
   - Columns: Time, Type, Camera, Severity, Status, Actions
   - Sortable columns
   - Pagination

2. **Build Alerts Page** (`app/alerts/page.tsx`)
   - Filter bar (date range, type, severity)
   - Alert table
   - "Export CSV" button (non-functional for now)

3. **Create Alert Detail Modal** (`components/AlertDetailModal.tsx`)
   - Show full alert information
   - Display snapshot image
   - Acknowledge/Dismiss buttons

4. **Mock Alert History Data**
   ```typescript
   const mockAlertHistory = [
     { id: 1, timestamp: '2024-01-15 10:30', type: 'WEAPON', camera: 'Front', severity: 'CRITICAL', status: 'ACTIVE' },
     { id: 2, timestamp: '2024-01-15 09:15', type: 'PERSON', camera: 'Lobby', severity: 'WARNING', status: 'ACKNOWLEDGED' },
     // ... 20+ more entries
   ];
   ```

#### Visual Example: Alerts Page
```
┌─────────────────────────────────────────────────────────────┐
│  Alert History                              [Export CSV]     │
├─────────────────────────────────────────────────────────────┤
│  [Date Range ▼] [Type ▼] [Severity ▼] [Status ▼] [Search]  │
├─────────────────────────────────────────────────────────────┤
│  Time       │ Type    │ Camera  │ Severity │ Status │ ...   │
│  ──────────────────────────────────────────────────────────  │
│  10:30 AM   │ WEAPON  │ Front   │ 🔴 CRIT  │ ACTIVE │[View] │
│  09:15 AM   │ PERSON  │ Lobby   │ 🟠 WARN  │ ACK'D  │[View] │
│  08:45 AM   │ ZONE    │ Server  │ 🟠 WARN  │ ACK'D  │[View] │
│  ...                                                         │
├─────────────────────────────────────────────────────────────┤
│  Showing 1-10 of 156        [← Previous] [Next →]           │
└─────────────────────────────────────────────────────────────┘
```

#### Acceptance Criteria
- [ ] Table displays all mock alerts
- [ ] Sorting works (click column headers)
- [ ] Filters update the table
- [ ] Pagination works
- [ ] Detail modal opens on "View" click

---

## 🔌 API Integration Checklist (Post-Development)

Once backend Phase 2 is complete, replace mock data with real API calls:

### Cameras
```typescript
// Replace this:
const cameras = mockCameras;

// With this:
const response = await fetch('http://localhost:8000/api/v1/cameras');
const cameras = await response.json();
```

### Persons
```typescript
// Replace this:
const persons = mockPersons;

// With this:
const response = await fetch('http://localhost:8000/api/v1/persons');
const persons = await response.json();
```

### Alerts (Real-time)
```typescript
// Add WebSocket connection (Phase 3)
const ws = new WebSocket('ws://localhost:8000/ws/events');
ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  setAlerts(prev => [alert, ...prev]);
};
```

### Video Feed
```typescript
// Replace placeholder with real stream
<img src="http://localhost:8000/video_feed" alt="Live camera" />
```

---

## 📦 Deliverables Summary

| Phase | Deliverable | Files Created | Mock Data | API Ready |
|-------|-------------|---------------|-----------|-----------|
| 1 | Foundation | Layout, Navbar, Shared Components | N/A | N/A |
| 2 | Cameras | CameraCard, CameraForm, Cameras Page | ✅ | 🔌 |
| 3 | Persons | PersonCard, PersonForm, Persons Page | ✅ | 🔌 |
| 4 | Dashboard | VideoPlayer, AlertFeed, Dashboard Page | ✅ | 🔌 |
| 5 | Alerts | AlertTable, AlertDetailModal, Alerts Page | ✅ | 🔌 |

**Legend**: ✅ = Mock data included, 🔌 = API integration points marked

---

## ⏱️ Timeline Estimate

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| Phase 1: Foundation | 2-3 days | None |
| Phase 2: Cameras | 2 days | Phase 1 |
| Phase 3: Persons | 2 days | Phase 1 |
| Phase 4: Dashboard | 3 days | Phase 1 |
| Phase 5: Alerts | 2 days | Phase 1 |
| **Total** | **~2 weeks** | - |

---

## ✅ Success Criteria

Frontend Phase 2 is **COMPLETE** when:

1. ✅ All 5 pages are built and navigable
2. ✅ All components use mock data
3. ✅ Design is consistent (colors, spacing, typography)
4. ✅ Responsive on mobile, tablet, desktop
5. ✅ All API integration points are marked with `// TODO: API`
6. ✅ Code is committed to GitHub
7. ✅ Team can demo the UI to stakeholders

---

## 🚀 Next Steps (After Phase 2)

Once backend AI detection is ready:
1. Replace all mock data with real API calls
2. Add WebSocket for real-time alerts
3. Test end-to-end flow (detection → alert → UI)
4. Move to Phase 3: Zone Management & Advanced Features

---

**Ready to build!** 🎨
