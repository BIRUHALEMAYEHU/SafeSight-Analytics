"""
Tests for database models
"""
import pytest
from sqlalchemy import select
from app.models import User, Camera, Zone, PersonOfInterest, Event, Alert, Rule


class TestUserModel:
    """Test User model"""
    
    async def test_create_user(self, db_session):
        """Test creating a user"""
        user = User(
            username="testuser",
            hashed_password="hashed_password_123",
            email="test@example.com",
            full_name="Test User",
            role="operator",
            is_active=True
        )
        db_session.add(user)
        await db_session.commit()
        
        # Query back
        result = await db_session.execute(select(User).where(User.username == "testuser"))
        saved_user = result.scalar_one()
        
        assert saved_user.username == "testuser"
        assert saved_user.email == "test@example.com"
        assert saved_user.role == "operator"
        assert saved_user.is_active is True


class TestCameraModel:
    """Test Camera model"""
    
    async def test_create_camera(self, db_session):
        """Test creating a camera"""
        camera = Camera(
            name="Entrance Camera",
            rtsp_url="rtsp://192.168.1.100:554/stream",
            location="Main Entrance",
            is_active=True
        )
        db_session.add(camera)
        await db_session.commit()
        
        result = await db_session.execute(select(Camera).where(Camera.name == "Entrance Camera"))
        saved_camera = result.scalar_one()
        
        assert saved_camera.name == "Entrance Camera"
        assert saved_camera.rtsp_url == "rtsp://192.168.1.100:554/stream"
        assert saved_camera.location == "Main Entrance"


class TestZoneModel:
    """Test Zone model"""
    
    async def test_create_zone(self, db_session):
        """Test creating a zone with polygon"""
        # First create a camera
        camera = Camera(name="Test Camera", rtsp_url="rtsp://test", location="Test")
        db_session.add(camera)
        await db_session.commit()
        
        # Create zone
        zone = Zone(
            camera_id=camera.id,
            name="Restricted Area",
            type="restricted",
            polygon=[[0, 0], [100, 0], [100, 100], [0, 100]],
            is_active=True
        )
        db_session.add(zone)
        await db_session.commit()
        
        result = await db_session.execute(select(Zone).where(Zone.name == "Restricted Area"))
        saved_zone = result.scalar_one()
        
        assert saved_zone.name == "Restricted Area"
        assert saved_zone.type == "restricted"
        assert len(saved_zone.polygon) == 4
        assert saved_zone.camera_id == camera.id


class TestPersonOfInterestModel:
    """Test PersonOfInterest model"""
    
    async def test_create_person(self, db_session):
        """Test creating a person of interest"""
        person = PersonOfInterest(
            name="John Doe",
            type="wanted",
            photo_path="/photos/john_doe.jpg",
            face_encoding=[0.1] * 128,  # 128-d vector
            notes="Wanted for questioning",
            created_at="2025-01-01T00:00:00"
        )
        db_session.add(person)
        await db_session.commit()
        
        result = await db_session.execute(
            select(PersonOfInterest).where(PersonOfInterest.name == "John Doe")
        )
        saved_person = result.scalar_one()
        
        assert saved_person.name == "John Doe"
        assert saved_person.type == "wanted"
        assert len(saved_person.face_encoding) == 128


class TestEventModel:
    """Test Event model"""
    
    async def test_create_event(self, db_session):
        """Test creating an event"""
        # Create camera first
        camera = Camera(name="Test Camera", rtsp_url="rtsp://test", location="Test")
        db_session.add(camera)
        await db_session.commit()
        
        # Create event
        event = Event(
            camera_id=camera.id,
            type="person_detected",
            event_metadata={"confidence": 0.95, "bbox": [100, 200, 50, 50]},
            snapshot_path="/snapshots/event_123.jpg"
        )
        db_session.add(event)
        await db_session.commit()
        
        result = await db_session.execute(select(Event).where(Event.camera_id == camera.id))
        saved_event = result.scalar_one()
        
        assert saved_event.type == "person_detected"
        assert saved_event.event_metadata["confidence"] == 0.95


class TestAlertModel:
    """Test Alert model"""
    
    async def test_create_alert(self, db_session):
        """Test creating an alert"""
        # Create camera and event
        camera = Camera(name="Test Camera", rtsp_url="rtsp://test", location="Test")
        db_session.add(camera)
        await db_session.commit()
        
        event = Event(
            camera_id=camera.id,
            type="weapon_detected",
            event_metadata={},
            snapshot_path="/snapshots/alert.jpg"
        )
        db_session.add(event)
        await db_session.commit()
        
        # Create alert
        alert = Alert(
            event_id=event.id,
            type="weapon_alert",
            priority="critical",
            status="new"
        )
        db_session.add(alert)
        await db_session.commit()
        
        result = await db_session.execute(select(Alert).where(Alert.event_id == event.id))
        saved_alert = result.scalar_one()
        
        assert saved_alert.type == "weapon_alert"
        assert saved_alert.priority == "critical"
        assert saved_alert.status == "new"


class TestRuleModel:
    """Test Rule model"""
    
    async def test_create_rule(self, db_session):
        """Test creating a rule"""
        rule = Rule(
            name="Armed Person Alert",
            conditions={
                "all": [
                    {"field": "detection.label", "operator": "in", "value": ["gun", "knife"]},
                    {"field": "context.uniform_detected", "operator": "equals", "value": False}
                ]
            },
            action={
                "type": "alert",
                "priority": "critical",
                "message": "Armed person without uniform detected"
            },
            is_active=True
        )
        db_session.add(rule)
        await db_session.commit()
        
        result = await db_session.execute(select(Rule).where(Rule.name == "Armed Person Alert"))
        saved_rule = result.scalar_one()
        
        assert saved_rule.name == "Armed Person Alert"
        assert saved_rule.is_active is True
        assert saved_rule.action["priority"] == "critical"


class TestRelationships:
    """Test model relationships"""
    
    async def test_camera_zones_relationship(self, db_session):
        """Test Camera has many Zones"""
        camera = Camera(name="Test Camera", rtsp_url="rtsp://test", location="Test")
        db_session.add(camera)
        await db_session.commit()
        
        zone1 = Zone(camera_id=camera.id, name="Zone 1", type="restricted", polygon=[[0, 0]])
        zone2 = Zone(camera_id=camera.id, name="Zone 2", type="safe", polygon=[[0, 0]])
        db_session.add_all([zone1, zone2])
        await db_session.commit()
        
        # Refresh camera to load relationships
        await db_session.refresh(camera, ["zones"])
        
        assert len(camera.zones) == 2
        assert camera.zones[0].name in ["Zone 1", "Zone 2"]
    
    async def test_event_alert_relationship(self, db_session):
        """Test Event has many Alerts"""
        camera = Camera(name="Test Camera", rtsp_url="rtsp://test", location="Test")
        db_session.add(camera)
        await db_session.commit()
        
        event = Event(camera_id=camera.id, type="test", event_metadata={}, snapshot_path="/test")
        db_session.add(event)
        await db_session.commit()
        
        alert1 = Alert(event_id=event.id, type="alert1", priority="critical", status="new")
        alert2 = Alert(event_id=event.id, type="alert2", priority="warning", status="new")
        db_session.add_all([alert1, alert2])
        await db_session.commit()
        
        await db_session.refresh(event, ["alerts"])
        
        assert len(event.alerts) == 2
