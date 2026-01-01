"""
Face Analyzer Module
Handles face detection, encoding, and recognition using DeepFace
"""

from deepface import DeepFace
import numpy as np
import cv2
from typing import List, Dict, Optional
import httpx
import os


class FaceAnalyzer:
    """
    Face detection and recognition analyzer
    Uses DeepFace library with SFace model for face recognition
    """
    
    def __init__(self, backend_url: str = None):
        """
        Initialize the Face Analyzer
        
        Args:
            backend_url: URL of the backend API to fetch known persons
        """
        self.model_name = "SFace"
        self.backend_url = backend_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.known_persons = {}  # Cache of known persons {id: {name, type, encoding_path}}
        self.db_path = "./known_faces"  # Local cache directory
        
    async def load_known_persons(self):
        """
        Load known persons from backend API
        Downloads face images and stores them locally for DeepFace
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.backend_url}/api/v1/persons",
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    persons = response.json()
                    
                    # Create local cache directory
                    os.makedirs(self.db_path, exist_ok=True)
                    
                    for person in persons:
                        person_id = person.get("id")
                        person_name = person.get("name")
                        face_encoding_path = person.get("face_encoding_path")
                        
                        if face_encoding_path:
                            # Create person directory
                            person_dir = os.path.join(self.db_path, person_name)
                            os.makedirs(person_dir, exist_ok=True)
                            
                            # Store person info
                            self.known_persons[person_id] = {
                                "name": person_name,
                                "type": person.get("type", "NORMAL"),
                                "path": person_dir
                            }
                            
                    print(f"Loaded {len(self.known_persons)} known persons from database")
                else:
                    print(f"Failed to load persons from backend: {response.status_code}")
                    
        except Exception as e:
            print(f"Error loading known persons: {e}")
            # Fallback to file system if API fails
            self._load_from_filesystem()
    
    def _load_from_filesystem(self):
        """
        Fallback: Load known persons from file system
        Used when backend API is unavailable
        """
        if os.path.exists(self.db_path):
            for person_name in os.listdir(self.db_path):
                person_dir = os.path.join(self.db_path, person_name)
                if os.path.isdir(person_dir):
                    self.known_persons[person_name] = {
                        "name": person_name,
                        "type": "UNKNOWN",  # Type unknown from filesystem
                        "path": person_dir
                    }
            print(f"Loaded {len(self.known_persons)} persons from filesystem (fallback)")
    
    def analyze(self, frame: np.ndarray) -> List[Dict]:
        """
        Analyze a frame for faces
        
        Args:
            frame: Video frame as numpy array (BGR format)
            
        Returns:
            List of detection events with format:
            [
                {
                    "type": "face_detected",
                    "person_name": str,
                    "person_id": int (optional),
                    "person_type": str,
                    "confidence": float,
                    "bbox": [x, y, w, h]
                }
            ]
        """
        detections = []
        
        try:
            # Only analyze if we have known persons
            if not self.known_persons and os.path.exists(self.db_path):
                # Use DeepFace.find with local database
                results = DeepFace.find(
                    img_path=frame,
                    db_path=self.db_path,
                    enforce_detection=False,
                    silent=True,
                    model_name=self.model_name
                )
                
                # Process results
                for df in results:
                    if not df.empty:
                        row = df.iloc[0]
                        
                        # Extract person name from path
                        identity_path = row['identity']
                        person_name = identity_path.split(os.sep)[-2]
                        
                        # Find person info
                        person_info = None
                        for pid, info in self.known_persons.items():
                            if info["name"] == person_name:
                                person_info = info
                                break
                        
                        detection = {
                            "type": "face_detected",
                            "person_name": person_name,
                            "person_type": person_info.get("type", "UNKNOWN") if person_info else "UNKNOWN",
                            "confidence": float(1.0 - row.get('distance', 0.0)),  # Convert distance to confidence
                            "bbox": [
                                int(row['source_x']),
                                int(row['source_y']),
                                int(row['source_w']),
                                int(row['source_h'])
                            ]
                        }
                        
                        detections.append(detection)
                        
        except Exception as e:
            print(f"Face analysis error: {e}")
        
        return detections
    
    def detect_faces(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect faces without recognition (faster)
        
        Args:
            frame: Video frame as numpy array
            
        Returns:
            List of face bounding boxes
        """
        try:
            # Use DeepFace's built-in face detection
            faces = DeepFace.extract_faces(
                img_path=frame,
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            detections = []
            for face in faces:
                facial_area = face.get('facial_area', {})
                detections.append({
                    "bbox": [
                        facial_area.get('x', 0),
                        facial_area.get('y', 0),
                        facial_area.get('w', 0),
                        facial_area.get('h', 0)
                    ],
                    "confidence": face.get('confidence', 0.0)
                })
            
            return detections
            
        except Exception as e:
            print(f"Face detection error: {e}")
            return []
