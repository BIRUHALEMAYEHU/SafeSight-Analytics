# Frontend Implementation Plan - SafeSight Analytics

## The Vision

We're building a **high-end security operations center** - think CIA surveillance room, not a typical web dashboard. This is a mission-critical system where every second counts. The interface should feel powerful, focused, and professional.

### Core Philosophy
- **Dark theme**: Reduce eye strain during long monitoring sessions
- **Minimal distractions**: Only show what matters right now
- **Grid-first**: Cameras are the star of the show
- **Alert-driven**: Warnings demand immediate attention
- **Scalable**: Works on massive video walls or single laptops

---

## Main Dashboard (The Command Center)

This is where operators spend 90% of their time. It's all about the video feeds.

### What You See

```
┌────────────────────────────────────────────────────────────────┐
│ ☰  SAFESIGHT ANALYTICS                    🔴 LIVE  |  Admin ▼ │ ← Minimal top bar
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ [VIDEO]  │ │ [VIDEO]  │ │ [VIDEO]  │ │ [VIDEO]  │         │
│  │ CAM-01   │ │ CAM-02   │ │ CAM-03   │ │ CAM-04   │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ [VIDEO]  │ │ [VIDEO]  │ │ [VIDEO]  │ │ [VIDEO]  │         │
│  │ CAM-05   │ │ CAM-06   │ │ CAM-07   │ │ CAM-08   │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ [VIDEO]  │ │ [VIDEO]  │ │ [VIDEO]  │ │ [VIDEO]  │         │
│  │ CAM-09   │ │ CAM-10   │ │ CAM-11   │ │ CAM-12   │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                                                                │
├────────────────────────────────────────────────────────────────┤
│ [2x2] [3x3] [4x4] [5x5]    Page 1 of 3  [◀ Prev] [Next ▶]    │ ← Grid controls
│ 47 Cameras Online  |  12 Persons Monitored  |  Uptime: 72h    │ ← Status bar
└────────────────────────────────────────────────────────────────┘
```

### Key Features

**1. Hamburger Menu (Top Left)**
- Click to reveal side panel with navigation
- Cameras / Persons / Alerts / Settings
- Collapses back when you select a page

**2. Grid Layout Controls (Bottom)**
- Buttons to switch between 2x2, 3x3, 4x4, 5x5 layouts
- Automatically adjusts based on screen size
- On a 4K monitor? Show 5x5 (25 cameras at once)
- On a laptop? Default to 3x3 (9 cameras)

**3. Pagination (Bottom Center)**
- If you have 50 cameras but showing 12, you need pages
- "Page 1 of 5" with Previous/Next arrows
- Keyboard shortcuts: Arrow keys to navigate

**4. Status Bar (Bottom)**
- Simple text info: "47 Cameras Online | 12 Persons Monitored | Uptime: 72h"
- No clutter, just facts

**5. Alert Popup (When Triggered)**
```
┌────────────────────────────────────┐
│  ⚠️  CRITICAL ALERT                │
│                                    │
│  WEAPON DETECTED                   │
│  Camera: Front Entrance (CAM-03)   │
│  Confidence: 95%                   │
│  Time: 13:45:22                    │
│                                    │
│  [View Camera] [Acknowledge]       │
└────────────────────────────────────┘
```
- **Sound**: Plays a warning beep (configurable volume)
- **Overlay**: Appears in center of screen, semi-transparent dark background
- **Auto-dismiss**: After 10 seconds if not clicked
- **Click "View Camera"**: Jumps to that specific camera feed

---

## Color Palette

### Background Colors
- **Primary Background**: `#0A0E1A` (Deep navy, almost black)
- **Secondary Background**: `#1A1F2E` (Slightly lighter for cards)
- **Accent Background**: `#252B3B` (Hover states)

### Text Colors
- **Primary Text**: `#E5E7EB` (Off-white, easy on eyes)
- **Secondary Text**: `#9CA3AF` (Gray for labels)
- **Muted Text**: `#6B7280` (Timestamps, metadata)

### Status Colors
- **Active/Online**: `#10B981` (Green)
- **Inactive/Offline**: `#6B7280` (Gray)
- **Critical Alert**: `#EF4444` (Red)
- **Warning Alert**: `#F59E0B` (Amber)
- **Info**: `#3B82F6` (Blue)

### Accent Colors
- **Primary Action**: `#3B82F6` (Blue buttons)
- **Danger Action**: `#DC2626` (Delete, critical actions)
- **Success**: `#059669` (Confirmations)

### Visual Example
```css
/* Main background */
body { background: #0A0E1A; color: #E5E7EB; }

/* Video card */
.camera-card { 
  background: #1A1F2E; 
  border: 1px solid #252B3B;
}

/* Active camera indicator */
.status-online { color: #10B981; }

/* Critical alert */
.alert-critical { 
  background: rgba(239, 68, 68, 0.1);
  border-left: 4px solid #EF4444;
}
```

---

## Development Phases

### Phase 1: The Grid (Week 1)

**What we're building**: The main dashboard with video grid and controls.

**Files to create**:
- `app/page.tsx` - Main dashboard page
- `components/VideoGrid.tsx` - Grid container
- `components/VideoCard.tsx` - Single camera display
- `components/GridControls.tsx` - Layout switcher (2x2, 3x3, etc.)
- `components/StatusBar.tsx` - Bottom info bar

**Step-by-step**:

1. **Create the dark theme** (`app/globals.css`)
   ```css
   :root {
     --bg-primary: #0A0E1A;
     --bg-secondary: #1A1F2E;
     --text-primary: #E5E7EB;
     --status-online: #10B981;
     --alert-critical: #EF4444;
   }
   
   body {
     background: var(--bg-primary);
     color: var(--text-primary);
     font-family: 'Inter', sans-serif;
   }
   ```

2. **Build the VideoCard component**
   ```typescript
   // components/VideoCard.tsx
   export function VideoCard({ camera }) {
     return (
       <div className="bg-[#1A1F2E] rounded border border-[#252B3B] overflow-hidden">
         {/* Video placeholder for now */}
         <div className="aspect-video bg-black flex items-center justify-center">
           <span className="text-gray-500">CAM-{camera.id}</span>
         </div>
         
         {/* Camera label */}
         <div className="p-2 flex justify-between items-center">
           <span className="text-sm">{camera.name}</span>
           <span className="text-xs text-green-500">● LIVE</span>
         </div>
       </div>
     );
   }
   ```

3. **Build the VideoGrid component**
   ```typescript
   // components/VideoGrid.tsx
   export function VideoGrid({ cameras, layout = '3x3' }) {
     const gridCols = {
       '2x2': 'grid-cols-2',
       '3x3': 'grid-cols-3',
       '4x4': 'grid-cols-4',
       '5x5': 'grid-cols-5',
     };
     
     return (
       <div className={`grid ${gridCols[layout]} gap-4 p-4`}>
         {cameras.map(camera => (
           <VideoCard key={camera.id} camera={camera} />
         ))}
       </div>
     );
   }
   ```

4. **Build the GridControls component**
   ```typescript
   // components/GridControls.tsx
   export function GridControls({ currentLayout, onLayoutChange, currentPage, totalPages, onPageChange }) {
     return (
       <div className="flex items-center justify-between px-4 py-3 bg-[#1A1F2E] border-t border-[#252B3B]">
         {/* Layout buttons */}
         <div className="flex gap-2">
           {['2x2', '3x3', '4x4', '5x5'].map(layout => (
             <button
               key={layout}
               onClick={() => onLayoutChange(layout)}
               className={`px-3 py-1 rounded ${
                 currentLayout === layout 
                   ? 'bg-blue-600 text-white' 
                   : 'bg-[#252B3B] text-gray-400 hover:bg-[#2A3142]'
               }`}
             >
               {layout}
             </button>
           ))}
         </div>
         
         {/* Pagination */}
         <div className="flex items-center gap-4">
           <span className="text-sm text-gray-400">Page {currentPage} of {totalPages}</span>
           <button onClick={() => onPageChange(currentPage - 1)} disabled={currentPage === 1}>
             ◀ Prev
           </button>
           <button onClick={() => onPageChange(currentPage + 1)} disabled={currentPage === totalPages}>
             Next ▶
           </button>
         </div>
       </div>
     );
   }
   ```

5. **Build the StatusBar component**
   ```typescript
   // components/StatusBar.tsx
   export function StatusBar({ stats }) {
     return (
       <div className="px-4 py-2 bg-[#0A0E1A] border-t border-[#252B3B] text-sm text-gray-400">
         <span>{stats.camerasOnline} Cameras Online</span>
         <span className="mx-2">|</span>
         <span>{stats.personsMonitored} Persons Monitored</span>
         <span className="mx-2">|</span>
         <span>Uptime: {stats.uptime}</span>
       </div>
     );
   }
   ```

6. **Put it all together** (`app/page.tsx`)
   ```typescript
   'use client';
   import { useState } from 'react';
   import { VideoGrid } from '@/components/VideoGrid';
   import { GridControls } from '@/components/GridControls';
   import { StatusBar } from '@/components/StatusBar';
   
   export default function Dashboard() {
     const [layout, setLayout] = useState('3x3');
     const [currentPage, setCurrentPage] = useState(1);
     
     // TODO: API - Replace with real data
     const mockCameras = Array.from({ length: 50 }, (_, i) => ({
       id: i + 1,
       name: `Camera ${i + 1}`,
       isOnline: true,
     }));
     
     const camerasPerPage = parseInt(layout.split('x')[0]) ** 2;
     const totalPages = Math.ceil(mockCameras.length / camerasPerPage);
     const visibleCameras = mockCameras.slice(
       (currentPage - 1) * camerasPerPage,
       currentPage * camerasPerPage
     );
     
     return (
       <div className="h-screen flex flex-col">
         {/* Top bar */}
         <header className="bg-[#1A1F2E] px-4 py-3 flex justify-between items-center border-b border-[#252B3B]">
           <div className="flex items-center gap-4">
             <button className="text-2xl">☰</button>
             <h1 className="text-xl font-bold">SAFESIGHT ANALYTICS</h1>
           </div>
           <div className="flex items-center gap-4">
             <span className="text-red-500">● LIVE</span>
             <button>Admin ▼</button>
           </div>
         </header>
         
         {/* Video grid */}
         <main className="flex-1 overflow-auto">
           <VideoGrid cameras={visibleCameras} layout={layout} />
         </main>
         
         {/* Controls */}
         <GridControls
           currentLayout={layout}
           onLayoutChange={setLayout}
           currentPage={currentPage}
           totalPages={totalPages}
           onPageChange={setCurrentPage}
         />
         
         {/* Status bar */}
         <StatusBar stats={{
           camerasOnline: 47,
           personsMonitored: 12,
           uptime: '72h 15m',
         }} />
       </div>
     );
   }
   ```

**What you should see**:
- Dark, professional interface
- Grid of camera placeholders
- Buttons to switch between 2x2, 3x3, 4x4, 5x5
- Pagination working (if you have 50 cameras, you'll see "Page 1 of 6" in 3x3 mode)
- Status bar at bottom

**Checklist**:
- [ ] Dark theme applied
- [ ] Grid layout switches work
- [ ] Pagination works
- [ ] Responsive (works on different screen sizes)
- [ ] Looks professional, not "webby"

---

### Phase 2: Alert System (Week 1)

**What we're building**: The popup alert with sound.

**Files to create**:
- `components/AlertPopup.tsx` - The modal that appears
- `hooks/useAlertSound.ts` - Sound player hook
- `public/alert-sound.mp3` - Warning sound file

**Step-by-step**:

1. **Create the AlertPopup component**
   ```typescript
   // components/AlertPopup.tsx
   export function AlertPopup({ alert, onClose, onViewCamera }) {
     useEffect(() => {
       // Auto-dismiss after 10 seconds
       const timer = setTimeout(onClose, 10000);
       return () => clearTimeout(timer);
     }, [onClose]);
     
     return (
       <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
         <div className="bg-[#1A1F2E] border-2 border-red-500 rounded-lg p-6 max-w-md animate-pulse-border">
           {/* Alert icon */}
           <div className="text-center mb-4">
             <span className="text-6xl">⚠️</span>
             <h2 className="text-2xl font-bold text-red-500 mt-2">CRITICAL ALERT</h2>
           </div>
           
           {/* Alert details */}
           <div className="space-y-2 text-center mb-6">
             <p className="text-xl font-semibold">{alert.type}</p>
             <p className="text-gray-400">Camera: {alert.cameraName} ({alert.cameraId})</p>
             <p className="text-gray-400">Confidence: {alert.confidence}%</p>
             <p className="text-gray-400">Time: {alert.timestamp}</p>
           </div>
           
           {/* Actions */}
           <div className="flex gap-3">
             <button
               onClick={onViewCamera}
               className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded"
             >
               View Camera
             </button>
             <button
               onClick={onClose}
               className="flex-1 bg-gray-700 hover:bg-gray-600 text-white py-2 rounded"
             >
               Acknowledge
             </button>
           </div>
         </div>
       </div>
     );
   }
   ```

2. **Add sound hook**
   ```typescript
   // hooks/useAlertSound.ts
   import { useEffect, useRef } from 'react';
   
   export function useAlertSound() {
     const audioRef = useRef<HTMLAudioElement | null>(null);
     
     useEffect(() => {
       audioRef.current = new Audio('/alert-sound.mp3');
     }, []);
     
     const play = () => {
       audioRef.current?.play();
     };
     
     return { play };
   }
   ```

3. **Integrate into dashboard**
   ```typescript
   // app/page.tsx (add this)
   const [activeAlert, setActiveAlert] = useState(null);
   const { play: playAlertSound } = useAlertSound();
   
   // Simulate alert (for testing)
   useEffect(() => {
     const timer = setTimeout(() => {
       const mockAlert = {
         type: 'WEAPON DETECTED',
         cameraName: 'Front Entrance',
         cameraId: 'CAM-03',
         confidence: 95,
         timestamp: new Date().toLocaleTimeString(),
       };
       setActiveAlert(mockAlert);
       playAlertSound();
     }, 5000); // Alert after 5 seconds
     
     return () => clearTimeout(timer);
   }, []);
   
   return (
     <div className="h-screen flex flex-col">
       {/* ... existing code ... */}
       
       {/* Alert popup */}
       {activeAlert && (
         <AlertPopup
           alert={activeAlert}
           onClose={() => setActiveAlert(null)}
           onViewCamera={() => {
             // TODO: Jump to camera
             setActiveAlert(null);
           }}
         />
       )}
     </div>
   );
   ```

4. **Add pulsing border animation** (`app/globals.css`)
   ```css
   @keyframes pulse-border {
     0%, 100% { border-color: #EF4444; }
     50% { border-color: #FCA5A5; }
   }
   
   .animate-pulse-border {
     animation: pulse-border 1s ease-in-out infinite;
   }
   ```

**What you should see**:
- After 5 seconds, a popup appears in the center
- Sound plays (make sure you have `alert-sound.mp3` in `public/`)
- Border pulses red
- Auto-dismisses after 10 seconds
- Can click "Acknowledge" to close early

**Checklist**:
- [ ] Popup appears centered
- [ ] Sound plays
- [ ] Border pulses
- [ ] Auto-dismiss works
- [ ] Buttons work

---

### Phase 3: Navigation Menu (Week 2)

**What we're building**: The hamburger menu to access other pages.

**Files to create**:
- `components/Sidebar.tsx` - Slide-out menu
- `app/cameras/page.tsx` - Camera management page
- `app/persons/page.tsx` - Persons page
- `app/alerts/page.tsx` - Alerts history page

**Step-by-step**:

1. **Create Sidebar component**
   ```typescript
   // components/Sidebar.tsx
   export function Sidebar({ isOpen, onClose }) {
     return (
       <>
         {/* Backdrop */}
         {isOpen && (
           <div
             className="fixed inset-0 bg-black/50 z-40"
             onClick={onClose}
           />
         )}
         
         {/* Sidebar */}
         <div
           className={`fixed top-0 left-0 h-full w-64 bg-[#1A1F2E] border-r border-[#252B3B] z-50 transform transition-transform ${
             isOpen ? 'translate-x-0' : '-translate-x-full'
           }`}
         >
           <div className="p-4">
             <h2 className="text-xl font-bold mb-6">SAFESIGHT</h2>
             
             <nav className="space-y-2">
               <a href="/" className="block px-4 py-2 rounded hover:bg-[#252B3B]">
                 📹 Live Monitoring
               </a>
               <a href="/cameras" className="block px-4 py-2 rounded hover:bg-[#252B3B]">
                 🎥 Cameras
               </a>
               <a href="/persons" className="block px-4 py-2 rounded hover:bg-[#252B3B]">
                 👤 Persons of Interest
               </a>
               <a href="/alerts" className="block px-4 py-2 rounded hover:bg-[#252B3B]">
                 ⚠️ Alert History
               </a>
               <a href="/settings" className="block px-4 py-2 rounded hover:bg-[#252B3B]">
                 ⚙️ Settings
               </a>
             </nav>
           </div>
         </div>
       </>
     );
   }
   ```

2. **Add to dashboard** (`app/page.tsx`)
   ```typescript
   const [sidebarOpen, setSidebarOpen] = useState(false);
   
   return (
     <div className="h-screen flex flex-col">
       <header className="...">
         <button onClick={() => setSidebarOpen(true)}>☰</button>
         {/* ... */}
       </header>
       
       <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
       
       {/* ... rest of dashboard ... */}
     </div>
   );
   ```

**What you should see**:
- Click hamburger menu → sidebar slides in from left
- Click outside → sidebar closes
- Links are visible (they won't work yet, we'll build those pages next)

**Checklist**:
- [ ] Sidebar slides in/out smoothly
- [ ] Backdrop darkens screen
- [ ] Click outside closes sidebar
- [ ] Links are styled correctly

---

### Phase 4: Other Pages (Week 2)

**What we're building**: Camera management, Persons, and Alerts pages.

These pages should follow the same dark, professional aesthetic but are simpler than the main dashboard.

**Camera Management Page** (`app/cameras/page.tsx`):
```
┌────────────────────────────────────────────────────────────────┐
│ ☰  CAMERAS                                        [+ Add]      │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ CAM-01  |  Front Entrance  |  Building A  |  🟢 Online │   │
│  │ [Edit] [Delete]                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ CAM-02  |  Parking Lot     |  Building B  |  🔴 Offline│   │
│  │ [Edit] [Delete]                                        │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Persons Page** (`app/persons/page.tsx`):
```
┌────────────────────────────────────────────────────────────────┐
│ ☰  PERSONS OF INTEREST                            [+ Add]      │
├────────────────────────────────────────────────────────────────┤
│  [All] [🔴 WANTED] [🟢 VIP] [🟠 BANNED]                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  [IMG]   │  │  [IMG]   │  │  [IMG]   │  │  [IMG]   │      │
│  │ John Doe │  │ Jane S.  │  │ Bob J.   │  │ Alice W. │      │
│  │🔴 WANTED │  │🟢 VIP    │  │🟠 BANNED │  │🔴 WANTED │      │
│  │ [View]   │  │ [View]   │  │ [View]   │  │ [View]   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

**Alerts History** (`app/alerts/page.tsx`):
```
┌────────────────────────────────────────────────────────────────┐
│ ☰  ALERT HISTORY                                               │
├────────────────────────────────────────────────────────────────┤
│  [Today] [This Week] [This Month] [All Time]                   │
├────────────────────────────────────────────────────────────────┤
│  Time     │ Type          │ Camera        │ Severity │ Status  │
│  ─────────────────────────────────────────────────────────────  │
│  13:45    │ WEAPON        │ Front (CAM-03)│ 🔴 CRIT  │ ACK'D   │
│  12:30    │ PERSON (Doe)  │ Lobby (CAM-09)│ 🟠 WARN  │ ACK'D   │
│  11:15    │ ZONE BREACH   │ Server (CAM-12│ 🟠 WARN  │ ACTIVE  │
│  ...                                                            │
└────────────────────────────────────────────────────────────────┘
```

I'll keep these simple - just lists/tables with the same dark theme. The focus is on clarity and speed.

**Checklist for each page**:
- [ ] Uses same dark color scheme
- [ ] Header with hamburger menu
- [ ] Clean, minimal design
- [ ] Mock data displays correctly
- [ ] Buttons/links are styled

---

## Mock Data Strategy

For all pages, use realistic mock data that matches the backend API format:

```typescript
// Mock cameras
const mockCameras = [
  { id: 'CAM-01', name: 'Front Entrance', location: 'Building A', rtsp_url: 'rtsp://...', is_active: true },
  { id: 'CAM-02', name: 'Parking Lot', location: 'Building B', rtsp_url: 'rtsp://...', is_active: false },
  // ... 50 total
];

// Mock persons
const mockPersons = [
  { id: 1, name: 'John Doe', type: 'WANTED', photo_path: '/mock/john.jpg', notes: 'Armed robbery suspect' },
  { id: 2, name: 'Jane Smith', type: 'VIP', photo_path: '/mock/jane.jpg', notes: 'CEO' },
  // ... 20 total
];

// Mock alerts
const mockAlerts = [
  { id: 1, timestamp: '2024-01-15 13:45', type: 'WEAPON', camera: 'CAM-03', severity: 'CRITICAL', status: 'ACKNOWLEDGED' },
  { id: 2, timestamp: '2024-01-15 12:30', type: 'PERSON', camera: 'CAM-09', person: 'John Doe', severity: 'WARNING', status: 'ACKNOWLEDGED' },
  // ... 100 total
];
```

Mark every place where you use mock data:
```typescript
// TODO: API - Replace with fetch('http://localhost:8000/api/v1/cameras')
const cameras = mockCameras;
```

---

## Timeline

| Phase | What | Days |
|-------|------|------|
| 1 | Video grid + controls | 3 |
| 2 | Alert popup + sound | 2 |
| 3 | Navigation menu | 1 |
| 4 | Other pages | 4 |
| **Total** | | **~10 days** |

---

## Success Criteria

You're done when:
- [ ] Main dashboard shows video grid
- [ ] Can switch between 2x2, 3x3, 4x4, 5x5 layouts
- [ ] Pagination works (can navigate through 50+ cameras)
- [ ] Alert popup appears with sound
- [ ] Hamburger menu opens sidebar
- [ ] All pages are accessible and styled
- [ ] Everything uses the dark, professional theme
- [ ] Looks like a CIA command center, not a web app

---

## Design Notes

**Fonts**: Use `Inter` or `Roboto Mono` for that technical, serious look.

**Spacing**: Keep it tight. This isn't a marketing site, it's a tool.

**Animations**: Minimal. Only use them for alerts or state changes.

**Icons**: Use simple emoji or Unicode symbols (📹 🔴 ⚠️) - no need for icon libraries yet.

**Sounds**: Find a professional alert sound (not a phone notification). Think submarine sonar ping or military radio beep.

---

That's it. Build this, and you'll have a dashboard that looks like it belongs in a high-security facility. No fluff, just function.
