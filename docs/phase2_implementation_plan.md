# Phase 2 Implementation Plan - Core Vision Modules

## Goal
Implement the foundational AI detection capabilities that transform raw video into actionable intelligence. This phase focuses on **Face Recognition** and **Object Detection** with a basic rules engine to trigger alerts.

---

## Theoretical Foundations

### 1. Face Recognition Pipeline

#### 1.1 Face Detection (Finding the Face)
**Algorithm**: Histogram of Oriented Gradients (HOG) or CNN-based detector
- **How it works**: 
  - HOG: Analyzes gradients (changes in brightness) to find face-like patterns
  - CNN: Uses a trained neural network to locate faces regardless of angle/lighting
- **Output**: Bounding box coordinates `(x, y, width, height)` for each detected face

#### 1.2 Face Alignment (Normalizing the Face)
**Algorithm**: 68-point facial landmark detection
- **How it works**: 
  - Identifies key points: eyes, nose tip, mouth corners, jawline
  - Applies affine transformation to "straighten" the face (eyes horizontal, centered)
- **Why**: Ensures consistent encoding regardless of head tilt

#### 1.3 Face Encoding (Creating the "Fingerprint")
**Algorithm**: Deep Residual Network (ResNet-34)
- **How it works**:
  - Passes the aligned face through 34 layers of convolutional neural network
  - Final layer outputs a **128-dimensional vector** (the "face encoding")
  - This vector represents unique facial features in mathematical space
- **Key Property**: Faces of the same person produce similar vectors (small Euclidean distance)

#### 1.4 Face Matching (Identification)
**Algorithm**: Euclidean Distance Comparison
- **Formula**: `distance = sqrt(sum((encoding1[i] - encoding2[i])^2))`
- **Decision Rule**:
  - If `distance < 0.6`: **MATCH** (Same person)
  - If `distance >= 0.6`: **NO MATCH** (Different person)
- **Why 0.6?**: Empirically determined threshold that balances false positives vs false negatives

---

### 2. Object Detection (YOLOv8)

#### 2.1 YOLO Architecture
**Algorithm**: You Only Look Once v8 (Single-shot detector)
- **How it works**:
  1. Divides image into a grid (e.g., 13x13)
  2. Each grid cell predicts:
     - **Bounding boxes** (x, y, w, h)
     - **Confidence scores** (probability of object presence)
     - **Class probabilities** (person, gun, knife, etc.)
  3. Applies Non-Maximum Suppression (NMS) to remove duplicate detections

#### 2.2 Classes We Detect
- **Person**: For crowd counting, zone intrusion
- **Gun**: Firearm detection
- **Knife**: Blade/weapon detection

#### 2.3 Confidence Threshold
- **Minimum confidence**: 0.5 (50%)
- **Rationale**: Balance between catching threats and avoiding false alarms

---

## System Architecture

### Module Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Vision Service                          │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │ Video Input  │───▶│ Frame Queue  │──▶│  Analyzers   │  │
│  │  (Camera)    │    │  (Buffer)    │   │              │  │
│  └──────────────┘    └──────────────┘   │ ┌──────────┐ │  │
│                                          │ │  Face    │ │  │
│                                          │ │ Analyzer │ │  │
│                                          │ └──────────┘ │  │
│                                          │ ┌──────────┐ │  │
│                                          │ │ Object   │ │  │
│                                          │ │ Analyzer │ │  │
│                                          │ └──────────┘ │  │
│                                          └──────┬───────┘  │
│                                                 │          │
│                                                 ▼          │
│                                          ┌──────────────┐  │
│                                          │ Event Queue  │  │
│                                          └──────┬───────┘  │
└─────────────────────────────────────────────────┼──────────┘
                                                  │
                                                  │ HTTP POST
                                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend Service                         │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐   ┌──────────────┐  │
│  │ Event        │───▶│ Rules Engine │──▶│ Alert        │  │
│  │ Receiver     │    │              │   │ Generator    │  │
│  └──────────────┘    └──────────────┘   └──────┬───────┘  │
│                                                 │          │
│                                                 ▼          │
│                                          ┌──────────────┐  │
│                                          │  Database    │  │
│                                          │  (Postgres)  │  │
│                                          └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Video Capture**: Camera → OpenCV → Frame (numpy array)
2. **Analysis**: Frame → Analyzers → Events (JSON)
3. **Event Transmission**: Vision → Backend (HTTP POST)
4. **Rule Evaluation**: Backend → Rules Engine → Alert Decision
5. **Storage**: Backend → Database (Alert record)
6. **Notification**: Backend → Frontend (WebSocket - Phase 3)

---

## Deliverables

### 1. Face Analyzer Module
**File**: `vision/analyzers/face_analyzer.py`

**Responsibilities**:
- Detect faces in frame
- Encode detected faces
- Compare against known persons database
- Generate "Person Identified" events

**Key Methods**:
```python
class FaceAnalyzer:
    def __init__(self, known_persons: List[Person]):
        """Load known face encodings from database"""
        
    def analyze(self, frame: np.ndarray) -> List[Event]:
        """Process frame and return face detection events"""
        
    def _detect_faces(self, frame) -> List[BoundingBox]:
        """Find all faces in frame"""
        
    def _encode_face(self, face_image) -> np.ndarray:
        """Generate 128-d encoding"""
        
    def _match_face(self, encoding) -> Optional[Person]:
        """Compare against known persons"""
```

### 2. Object Analyzer Module
**File**: `vision/analyzers/object_analyzer.py`

**Responsibilities**:
- Detect objects (person, gun, knife)
- Filter by confidence threshold
- Generate "Object Detected" events

**Key Methods**:
```python
class ObjectAnalyzer:
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        """Load YOLOv8 model"""
        
    def analyze(self, frame: np.ndarray) -> List[Event]:
        """Process frame and return object detection events"""
        
    def _detect_objects(self, frame) -> List[Detection]:
        """Run YOLO inference"""
        
    def _filter_detections(self, detections) -> List[Detection]:
        """Apply confidence threshold and class filter"""
```

### 3. Event Schema
**File**: `vision/models/event.py`

```python
class Event:
    type: str  # "face_detected", "object_detected"
    camera_id: str
    timestamp: datetime
    confidence: float
    bounding_box: BoundingBox
    metadata: dict  # e.g., {"person_name": "John Doe", "object_class": "gun"}
    snapshot: bytes  # Cropped image of detection
```

### 4. Basic Rules Engine
**File**: `backend/app/services/rules_engine.py`

**Rules**:
1. **IF** `event.type == "face_detected"` **AND** `person.type == "WANTED"` **THEN** create CRITICAL alert
2. **IF** `event.type == "object_detected"` **AND** `object_class == "gun"` **THEN** create CRITICAL alert
3. **IF** `event.type == "object_detected"` **AND** `object_class == "knife"` **THEN** create WARNING alert

### 5. Backend Event Endpoint
**File**: `backend/app/api/api_v1/endpoints/events.py`

```python
@router.post("/events")
async def receive_event(event: EventCreate, db: AsyncSession):
    """
    Receive event from Vision service
    1. Validate event
    2. Run through rules engine
    3. Create alert if rule triggers
    4. Store event in database
    """
```

---

## Implementation Steps

### Step 1: Install AI Libraries
**Duration**: 30 minutes

```bash
# In vision/ directory
pip install face_recognition dlib ultralytics
```

**Verification**:
```python
import face_recognition
import cv2
from ultralytics import YOLO
print("All libraries loaded successfully")
```

---

### Step 2: Build Face Analyzer
**Duration**: 2-3 hours

**Sub-tasks**:
1. Create `vision/analyzers/` directory
2. Implement `face_analyzer.py`:
   - Load known persons from backend API
   - Implement detection pipeline
   - Handle edge cases (no face, multiple faces)
3. Write unit tests with sample images
4. Test with live camera feed

**Test Case**:
```python
# Test: Detect known person
known_person = Person(name="John Doe", encoding=[...])
analyzer = FaceAnalyzer([known_person])
frame = cv2.imread("test_john.jpg")
events = analyzer.analyze(frame)
assert len(events) == 1
assert events[0].metadata["person_name"] == "John Doe"
```

---

### Step 3: Build Object Analyzer
**Duration**: 2-3 hours

**Sub-tasks**:
1. Download YOLOv8 model (`yolov8n.pt` - nano version for speed)
2. Implement `object_analyzer.py`:
   - Load YOLO model
   - Filter for relevant classes (person, gun, knife)
   - Apply confidence threshold
3. Write unit tests
4. Test with live camera feed

**Test Case**:
```python
# Test: Detect weapon
analyzer = ObjectAnalyzer(confidence_threshold=0.5)
frame = cv2.imread("test_gun.jpg")
events = analyzer.analyze(frame)
assert any(e.metadata["object_class"] == "gun" for e in events)
```

---

### Step 4: Integrate Analyzers into Vision Service
**Duration**: 2 hours

**File**: `vision/main.py`

**Changes**:
```python
from analyzers.face_analyzer import FaceAnalyzer
from analyzers.object_analyzer import ObjectAnalyzer

# Initialize analyzers
face_analyzer = FaceAnalyzer(load_known_persons())
object_analyzer = ObjectAnalyzer()

while True:
    ret, frame = camera.read()
    
    # Run analyzers
    face_events = face_analyzer.analyze(frame)
    object_events = object_analyzer.analyze(frame)
    
    # Send events to backend
    for event in face_events + object_events:
        send_event_to_backend(event)
```

---

### Step 5: Build Rules Engine
**Duration**: 2 hours

**File**: `backend/app/services/rules_engine.py`

**Implementation**:
```python
class RulesEngine:
    def evaluate(self, event: Event, db: AsyncSession) -> Optional[Alert]:
        """
        Evaluate event against all rules
        Return Alert if any rule triggers
        """
        if event.type == "face_detected":
            person = await get_person_by_name(event.metadata["person_name"], db)
            if person and person.type == "WANTED":
                return Alert(
                    type="PERSON_OF_INTEREST",
                    priority="CRITICAL",
                    event_id=event.id
                )
        
        if event.type == "object_detected":
            if event.metadata["object_class"] == "gun":
                return Alert(
                    type="WEAPON_DETECTED",
                    priority="CRITICAL",
                    event_id=event.id
                )
        
        return None
```

---

### Step 6: Create Backend Event Endpoint
**Duration**: 1 hour

**File**: `backend/app/api/api_v1/endpoints/events.py`

**Implementation**:
```python
@router.post("/", response_model=EventResponse)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db)
):
    # Store event
    event = Event(**event_in.dict())
    db.add(event)
    await db.commit()
    
    # Run rules engine
    rules_engine = RulesEngine()
    alert = await rules_engine.evaluate(event, db)
    
    if alert:
        db.add(alert)
        await db.commit()
    
    return event
```

---

### Step 7: End-to-End Testing
**Duration**: 2 hours

**Test Scenarios**:

1. **Scenario: Known Person Detection**
   - Upload photo of yourself as "Person of Interest"
   - Stand in front of camera
   - **Expected**: Alert created in database with your name

2. **Scenario: Weapon Detection**
   - Hold a toy gun or banana (for testing)
   - Point at camera
   - **Expected**: Alert created with type "WEAPON_DETECTED"

3. **Scenario: Unknown Person**
   - Have a friend stand in front of camera
   - **Expected**: Face detected but no alert (not in database)

4. **Scenario: No Detection**
   - Empty room
   - **Expected**: No events, no alerts

---

## Acceptance Criteria

### Face Recognition
- [ ] Can detect faces with >95% accuracy in good lighting
- [ ] Can identify known persons with <10% false positive rate
- [ ] Processes at least 10 FPS on standard hardware
- [ ] Handles multiple faces in single frame
- [ ] Gracefully handles no-face scenarios

### Object Detection
- [ ] Detects weapons with >90% accuracy
- [ ] Confidence threshold prevents excessive false alarms
- [ ] Processes at least 15 FPS
- [ ] Correctly filters for target classes (person, gun, knife)

### Integration
- [ ] Vision service successfully sends events to backend
- [ ] Backend stores events in database
- [ ] Rules engine correctly triggers alerts
- [ ] System runs continuously without crashes for 1 hour
- [ ] Alerts appear in database within 2 seconds of detection

---

## Performance Targets

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Face Detection Accuracy | >95% | Test with 100 sample images |
| Face Recognition Accuracy | >90% | Test with 50 known persons |
| Object Detection Accuracy | >90% | Test with 100 weapon images |
| Processing Speed (Face) | >10 FPS | Measure with `time.time()` |
| Processing Speed (Object) | >15 FPS | Measure with `time.time()` |
| End-to-End Latency | <2 seconds | Detection → Alert in DB |
| False Positive Rate | <10% | Manual review of 100 alerts |

---

## Risk Mitigation

### Risk 1: Poor Detection in Low Light
**Mitigation**: 
- Add image preprocessing (histogram equalization, brightness adjustment)
- Test with IR cameras if available
- Set minimum confidence threshold

### Risk 2: High False Positive Rate
**Mitigation**:
- Tune confidence thresholds based on real-world testing
- Implement "cooldown" period (don't alert same person every frame)
- Add manual review workflow for alerts

### Risk 3: Performance Issues
**Mitigation**:
- Use smaller YOLO model (yolov8n instead of yolov8x)
- Reduce frame processing rate (process every 2nd or 3rd frame)
- Use GPU acceleration if available

### Risk 4: Database Connection Failures
**Mitigation**:
- Implement event queue with retry logic
- Cache known persons locally in Vision service
- Add health check endpoint

---

## Dependencies

### External Libraries
- `face_recognition` (v1.3.0+)
- `dlib` (v19.24+)
- `ultralytics` (v8.0+) - YOLOv8
- `opencv-python` (already installed)
- `numpy` (already installed)

### Internal Dependencies
- Phase 1 must be complete (Database, API, Video pipeline)
- Backend `/api/persons` endpoint must be functional
- Database must be accessible from Vision service

---

## Timeline Estimate

| Task | Duration | Dependencies |
|------|----------|--------------|
| Install Libraries | 30 min | - |
| Face Analyzer | 3 hours | Libraries |
| Object Analyzer | 3 hours | Libraries |
| Integration | 2 hours | Both Analyzers |
| Rules Engine | 2 hours | Backend API |
| Event Endpoint | 1 hour | Rules Engine |
| Testing | 2 hours | All above |
| **Total** | **~14 hours** | - |

**Recommended Schedule**: 2-3 working days with breaks

---

## Success Metrics

Phase 2 is considered **COMPLETE** when:

1. ✅ All acceptance criteria are met
2. ✅ End-to-end demo works (person detection → alert in database)
3. ✅ Code is committed to GitHub
4. ✅ Team can run the system locally
5. ✅ Documentation is updated with setup instructions

---

## Next Phase Preview

**Phase 3: Advanced Scenario Logic** will build on this foundation:
- Zone management (draw restricted areas on camera feed)
- Crowd counting (count people in specific zones)
- Context rules (armed + no uniform = high alert)

But first, let's make Phase 2 rock-solid! 🚀
