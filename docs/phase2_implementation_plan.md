# Phase 2: Building the AI Brain

## What We're Actually Building

Right now, our system can stream video. That's it. It's just a fancy webcam viewer.

Phase 2 is where we add the **intelligence**. We're teaching the system to:
- Recognize faces (Who is this person?)
- Detect objects (Is that a weapon?)
- Make decisions (Should we alert someone?)

By the end of this phase, the system will watch the cameras 24/7 and automatically flag anything suspicious.

---

## What Phase 1 Already Gave Us

Before we start, let's confirm we have everything we need from Phase 1:

### Infrastructure ✅
- **Docker setup**: Database, backend, frontend all configured
- **Python 3.11**: Installed in `venv311` (because 3.14 broke everything)
- **Video pipeline**: We can capture frames from cameras
- **Database**: All tables created (cameras, persons, alerts, events)

### Backend API ✅
- **Camera endpoints**: `/api/v1/cameras` (add, list, edit, delete)
- **Person endpoints**: `/api/v1/persons` (manage who we're watching for)
- **Video streaming**: `/video_feed` works (we tested it!)

### What's Missing
- **WebSockets**: We'll add this in Phase 3 for real-time alerts
- **AI models**: That's what we're building now

If any of the above isn't working, **stop here** and fix it first. Everything in Phase 2 depends on this foundation.

---

## How Face Recognition Actually Works

Let me break down the theory without the academic jargon.

### Step 1: Find the Face
**Algorithm**: HOG (Histogram of Oriented Gradients) or CNN

Think of it like this: The algorithm looks for patterns of light and dark that match a face shape. Eyes are darker than the forehead. The nose casts a shadow. It's looking for these patterns.

**Output**: A box around the face with coordinates (x, y, width, height)

### Step 2: Straighten the Face
**Algorithm**: 68-point facial landmark detection

The algorithm finds 68 specific points on the face (corners of eyes, tip of nose, etc.). Then it rotates and scales the image so the eyes are horizontal and centered. This ensures we're always comparing "apples to apples" even if someone tilts their head.

**Why this matters**: Without this step, the same person looking left vs looking right would seem like different people.

### Step 3: Create the "Fingerprint"
**Algorithm**: Deep ResNet (34-layer neural network)

This is the magic part. The neural network has been trained on millions of faces. It converts the face into a list of 128 numbers (called an "encoding" or "embedding"). These numbers represent unique facial features in a way that's consistent across different photos.

**Example**: 
- Your face might be: `[0.23, -0.45, 0.67, ..., 0.12]` (128 numbers)
- My face might be: `[-0.12, 0.89, -0.34, ..., 0.56]` (completely different)

### Step 4: Compare and Match
**Algorithm**: Euclidean distance

To check if two faces are the same person, we calculate the "distance" between their encodings:

```
distance = sqrt((encoding1[0] - encoding2[0])² + (encoding1[1] - encoding2[1])² + ... + (encoding1[127] - encoding2[127])²)
```

**Decision rule**:
- If distance < 0.6: **Same person** ✅
- If distance >= 0.6: **Different person** ❌

**Why 0.6?** It's been tested on thousands of faces. Lower than 0.6 means too many false matches. Higher means we miss real matches.

---

## How Object Detection Works (YOLOv8)

YOLO stands for "You Only Look Once" - it's designed for speed.

### The Old Way (Slow)
Traditional object detection would:
1. Slide a window across the image
2. Check each window: "Is this a gun? No. Is this a gun? No. Is this a gun? Yes!"
3. Repeat thousands of times

This is **slow** (maybe 1-2 FPS).

### The YOLO Way (Fast)
YOLO looks at the entire image **once**:
1. Divide the image into a grid (e.g., 13x13 = 169 cells)
2. Each cell predicts: "Do I contain an object? If yes, what is it and where exactly?"
3. All predictions happen simultaneously

This is **fast** (30+ FPS on a decent computer).

### What We're Detecting
- **Person**: For counting people in zones
- **Gun**: Firearms
- **Knife**: Bladed weapons

### Confidence Threshold
We only trust detections above 50% confidence. Below that, it's probably a false alarm (like thinking a phone is a gun).

---

## The System Architecture

Here's how all the pieces fit together:

```
Camera → OpenCV → Frame (image)
                    ↓
            Face Analyzer → "Is this John Doe?"
                    ↓
           Object Analyzer → "Is this a weapon?"
                    ↓
              Event (JSON) → Send to Backend
                    ↓
            Rules Engine → "Should we alert?"
                    ↓
              Database → Store alert
```

### Data Flow Example

1. **Camera captures frame** (30 times per second)
2. **Face Analyzer processes it**:
   - Finds 2 faces
   - Encodes them
   - Compares to database of 50 known persons
   - Match found: "John Doe (WANTED)"
3. **Object Analyzer processes same frame**:
   - Detects 1 gun (95% confidence)
4. **Vision service sends event to Backend**:
   ```json
   {
     "type": "face_detected",
     "camera_id": "CAM-01",
     "timestamp": "2024-01-15T10:30:00Z",
     "person_name": "John Doe",
     "confidence": 0.87,
     "bounding_box": [100, 200, 50, 75]
   }
   ```
5. **Backend Rules Engine evaluates**:
   - "Person detected" + "Person type is WANTED" = **CRITICAL ALERT**
6. **Backend stores alert in database**
7. **Frontend shows popup** (Phase 3)

---

## What We're Building (The Deliverables)

### 1. Face Analyzer (`vision/analyzers/face_analyzer.py`)

**What it does**: Finds faces, encodes them, matches against known persons.

**Key functions**:
```python
class FaceAnalyzer:
    def analyze(self, frame):
        """Main entry point - process one frame"""
        # 1. Find all faces in frame
        # 2. Encode each face
        # 3. Compare to known persons
        # 4. Return list of events
        
    def _detect_faces(self, frame):
        """Find face locations"""
        
    def _encode_face(self, face_image):
        """Convert face to 128-d vector"""
        
    def _match_face(self, encoding):
        """Compare to database, return name if match"""
```

**Input**: A video frame (numpy array)  
**Output**: List of events (JSON objects)

### 2. Object Analyzer (`vision/analyzers/object_analyzer.py`)

**What it does**: Detects weapons and people using YOLOv8.

**Key functions**:
```python
class ObjectAnalyzer:
    def analyze(self, frame):
        """Main entry point - process one frame"""
        # 1. Run YOLO model
        # 2. Filter for our target classes (person, gun, knife)
        # 3. Filter by confidence (>50%)
        # 4. Return list of events
        
    def _detect_objects(self, frame):
        """Run YOLO inference"""
        
    def _filter_detections(self, detections):
        """Keep only high-confidence, relevant objects"""
```

**Input**: A video frame  
**Output**: List of events

### 3. Rules Engine (`backend/app/services/rules_engine.py`)

**What it does**: Decides if an event should trigger an alert.

**The rules** (for now, we keep it simple):
1. **IF** face detected **AND** person is WANTED → **CRITICAL alert**
2. **IF** gun detected → **CRITICAL alert**
3. **IF** knife detected → **WARNING alert**

Later (Phase 3), we'll add complex rules like "armed person + no uniform = high alert".

**Key function**:
```python
class RulesEngine:
    def evaluate(self, event):
        """Check if event triggers an alert"""
        # Look at event type and metadata
        # Apply rules
        # Return Alert object or None
```

### 4. Event Endpoint (`backend/app/api/api_v1/endpoints/events.py`)

**What it does**: Receives events from Vision service, runs rules, stores alerts.

**Endpoint**:
```python
@router.post("/events")
async def receive_event(event: EventCreate):
    # 1. Save event to database
    # 2. Run through rules engine
    # 3. If rule triggers, create alert
    # 4. Return success
```

---

## The Implementation Plan

### Step 1: Install the AI Libraries (30 minutes)

We need two main libraries:
- **face_recognition**: The easy-to-use wrapper
- **dlib**: The heavy-lifting engine (installed automatically with face_recognition)
- **ultralytics**: YOLOv8 implementation

```bash
# In the vision/ directory
pip install face_recognition ultralytics
```

**Test it works**:
```python
import face_recognition
from ultralytics import YOLO
print("Libraries loaded successfully!")
```

If this fails, you probably have Python version issues. Make sure you're using Python 3.11 (not 3.14).

---

### Step 2: Build the Face Analyzer (3 hours)

**Create the file**: `vision/analyzers/face_analyzer.py`

**What to build**:
1. **Load known persons** from backend API on startup
2. **Detect faces** in each frame
3. **Encode faces** into 128-d vectors
4. **Match faces** against known persons
5. **Generate events** for matches

**Test with**:
- A photo of yourself
- Add yourself to the database as "WANTED"
- Run the analyzer
- It should return: `{"person_name": "Your Name", "confidence": 0.85}`

**Edge cases to handle**:
- No face in frame (return empty list)
- Multiple faces (process all of them)
- Unknown face (don't generate event)

---

### Step 3: Build the Object Analyzer (3 hours)

**Create the file**: `vision/analyzers/object_analyzer.py`

**What to build**:
1. **Load YOLOv8 model** (download `yolov8n.pt` - the "nano" version for speed)
2. **Run detection** on each frame
3. **Filter results** (only keep person, gun, knife)
4. **Filter by confidence** (only keep >50%)
5. **Generate events** for detections

**Test with**:
- An image of a toy gun or banana (for testing)
- Run the analyzer
- It should return: `{"object_class": "gun", "confidence": 0.72}` (or similar)

**Performance tip**: YOLO is fast, but if you're processing 30 FPS, consider only running it on every 2nd or 3rd frame to save CPU.

---

### Step 4: Integrate into Vision Service (2 hours)

**Update**: `vision/main.py`

**What to change**:
```python
# Old code (just reads frames)
while True:
    ret, frame = camera.read()
    # ... do nothing ...

# New code (analyzes frames)
face_analyzer = FaceAnalyzer(known_persons)
object_analyzer = ObjectAnalyzer()

while True:
    ret, frame = camera.read()
    
    # Run analyzers
    face_events = face_analyzer.analyze(frame)
    object_events = object_analyzer.analyze(frame)
    
    # Send events to backend
    all_events = face_events + object_events
    for event in all_events:
        send_to_backend(event)  # HTTP POST to /api/v1/events
```

**Test**: Run the vision service. You should see events being sent to the backend in the logs.

---

### Step 5: Build the Rules Engine (2 hours)

**Create the file**: `backend/app/services/rules_engine.py`

**What to build**:
```python
class RulesEngine:
    async def evaluate(self, event, db):
        # Rule 1: Wanted person detected
        if event.type == "face_detected":
            person = await get_person_by_name(event.metadata["person_name"], db)
            if person and person.type == "WANTED":
                return Alert(
                    type="PERSON_OF_INTEREST",
                    priority="CRITICAL",
                    event_id=event.id
                )
        
        # Rule 2: Weapon detected
        if event.type == "object_detected":
            if event.metadata["object_class"] in ["gun", "knife"]:
                severity = "CRITICAL" if event.metadata["object_class"] == "gun" else "WARNING"
                return Alert(
                    type="WEAPON_DETECTED",
                    priority=severity,
                    event_id=event.id
                )
        
        return None  # No rule triggered
```

**Test**: Send a mock event to the backend. Check if an alert appears in the database.

---

### Step 6: Create the Event Endpoint (1 hour)

**Create the file**: `backend/app/api/api_v1/endpoints/events.py`

**What to build**:
```python
@router.post("/")
async def create_event(event_in: EventCreate, db: AsyncSession = Depends(get_db)):
    # Save event
    event = Event(**event_in.dict())
    db.add(event)
    await db.commit()
    
    # Check rules
    rules_engine = RulesEngine()
    alert = await rules_engine.evaluate(event, db)
    
    # Save alert if triggered
    if alert:
        db.add(alert)
        await db.commit()
    
    return {"status": "success", "alert_created": alert is not None}
```

**Test**: Use Postman or curl to POST a fake event. Check the database for the alert.

---

### Step 7: End-to-End Test (2 hours)

**The ultimate test**: Can the system detect you and create an alert?

**Setup**:
1. Add your photo to the database as a "WANTED" person
2. Start the backend
3. Start the vision service
4. Stand in front of the camera

**Expected result**:
- Vision service detects your face
- Encodes it
- Matches it to your database entry
- Sends event to backend
- Backend creates CRITICAL alert
- Alert appears in database within 2 seconds

**If it doesn't work**:
- Check logs for errors
- Verify your photo is in the database
- Make sure the camera can see your face clearly
- Check that the confidence threshold isn't too high

---

## How We Know We're Done

Phase 2 is complete when:

### Face Recognition
- [ ] Can detect faces in good lighting (>95% accuracy)
- [ ] Can identify known persons (<10% false positives)
- [ ] Runs at least 10 FPS
- [ ] Handles multiple faces in one frame
- [ ] Doesn't crash when there's no face

### Object Detection
- [ ] Detects weapons with >90% accuracy
- [ ] Runs at least 15 FPS
- [ ] Doesn't spam false alarms (confidence threshold works)
- [ ] Only detects our target classes (person, gun, knife)

### Integration
- [ ] Vision service sends events to backend successfully
- [ ] Backend stores events in database
- [ ] Rules engine triggers alerts correctly
- [ ] System runs for 1 hour without crashing
- [ ] Alert appears in database within 2 seconds of detection

### The Demo Test
- [ ] Upload your photo as "WANTED"
- [ ] Stand in front of camera
- [ ] Alert created in database with your name
- [ ] Hold a toy weapon
- [ ] Alert created for weapon detection

---

## Performance Targets

| What | Target | How to Measure |
|------|--------|----------------|
| Face detection accuracy | >95% | Test with 100 sample images |
| Face recognition accuracy | >90% | Test with 50 known persons |
| Object detection accuracy | >90% | Test with 100 weapon images |
| Face processing speed | >10 FPS | Use `time.time()` to measure |
| Object processing speed | >15 FPS | Use `time.time()` to measure |
| End-to-end latency | <2 seconds | Detection → Alert in DB |
| False positive rate | <10% | Manual review of 100 alerts |

---

## Potential Problems (And How to Fix Them)

### Problem 1: "It can't detect faces in low light"
**Fix**: 
- Add image preprocessing (brighten the image before detection)
- Lower the confidence threshold slightly
- Use better cameras with IR capability

### Problem 2: "Too many false alarms"
**Fix**:
- Increase confidence threshold (from 0.5 to 0.6 or 0.7)
- Add a "cooldown" period (don't alert on the same person every frame)
- Manually review alerts and tune the threshold

### Problem 3: "It's too slow"
**Fix**:
- Use the smaller YOLO model (`yolov8n` instead of `yolov8x`)
- Process every 2nd or 3rd frame instead of every frame
- Use GPU acceleration if available (CUDA)

### Problem 4: "Vision service can't connect to backend"
**Fix**:
- Check that backend is running
- Verify the URL is correct (`http://localhost:8000`)
- Add retry logic with exponential backoff

---

## Timeline

| Task | Time | Who |
|------|------|-----|
| Install libraries | 30 min | Anyone |
| Face Analyzer | 3 hours | AI team |
| Object Analyzer | 3 hours | AI team |
| Integration | 2 hours | AI team |
| Rules Engine | 2 hours | Backend team |
| Event Endpoint | 1 hour | Backend team |
| Testing | 2 hours | Everyone |
| **Total** | **~14 hours** | **2-3 days** |

---

## What Comes After This


**Phase 3** will add:
- **Zone management**: Draw restricted areas on camera feeds
- **Crowd counting**: Count people in specific zones
- **Context rules**: "Armed person + no uniform = high alert"
- **WebSockets**: Real-time alerts to frontend

