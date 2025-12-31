"""
Vision Service - SafeSight Analytics
Handles face detection and recognition using modular analyzers
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
import numpy as np
import cv2
import os
from analyzers.face_analyzer import FaceAnalyzer

# Configuration from environment variables
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
HOST = os.getenv("VISION_HOST", "0.0.0.0")
PORT = int(os.getenv("VISION_PORT", "8001"))

# Global analyzer instance
face_analyzer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    global face_analyzer
    
    # Startup: Initialize analyzers
    print("🚀 Starting Vision Service...")
    print(f"📡 Backend URL: {BACKEND_URL}")
    
    face_analyzer = FaceAnalyzer(backend_url=BACKEND_URL)
    
    # Load known persons from database
    print("📥 Loading known persons from database...")
    await face_analyzer.load_known_persons()
    
    print("✅ Vision Service ready!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Vision Service...")


app = FastAPI(
    title="SafeSight Vision Service",
    description="AI-powered face detection and recognition service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SafeSight Vision Service",
        "status": "running",
        "version": "1.0.0",
        "known_persons": len(face_analyzer.known_persons) if face_analyzer else 0
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "analyzer_loaded": face_analyzer is not None,
        "known_persons_count": len(face_analyzer.known_persons) if face_analyzer else 0,
        "backend_url": BACKEND_URL
    }


@app.post("/reload-persons")
async def reload_persons():
    """
    Reload known persons from database
    Useful when persons are added/updated in the backend
    """
    global face_analyzer
    
    if not face_analyzer:
        raise HTTPException(status_code=500, detail="Face analyzer not initialized")
    
    await face_analyzer.load_known_persons()
    
    return {
        "status": "success",
        "message": "Known persons reloaded",
        "count": len(face_analyzer.known_persons)
    }

# Set DeepFace home to local directory for portability
os.environ["DEEPFACE_HOME"] = './model'

@app.post("/analyze")
async def analyze_frame(file: UploadFile = File(...)):
    """
    Analyze a video frame for faces
    
    Args:
        file: Image file (JPEG/PNG)
        
    Returns:
        {
            "status": "success",
            "detections": [
                {
                    "name": str,
                    "type": str,
                    "confidence": float,
                    "x": int,
                    "y": int,
                    "distance": float (optional)
                }
            ]
        }
    """
    global face_analyzer
    
    if not face_analyzer:
        raise HTTPException(status_code=500, detail="Face analyzer not initialized")
    
    try:
        # Read and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Analyze frame using modular analyzer
        detections = face_analyzer.analyze(frame)
        
        # Format response for backward compatibility
        formatted_detections = []
        for detection in detections:
            formatted_detections.append({
                "name": detection.get("person_name", "Unknown"),
                "type": detection.get("person_type", "UNKNOWN"),
                "confidence": detection.get("confidence", 0.0),
                "x": detection["bbox"][0],
                "y": detection["bbox"][1],
                "w": detection["bbox"][2],
                "h": detection["bbox"][3]
            })
        
        return {
            "status": "success",
            "detections": formatted_detections,
            "count": len(formatted_detections)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "detections": []
        }


@app.post("/detect-only")
async def detect_faces_only(file: UploadFile = File(...)):
    """
    Detect faces without recognition (faster)
    
    Args:
        file: Image file (JPEG/PNG)
        
    Returns:
        List of face bounding boxes
    """
    global face_analyzer
    
    if not face_analyzer:
        raise HTTPException(status_code=500, detail="Face analyzer not initialized")
    
    try:
        # Read and decode image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Detect faces only (no recognition)
        detections = face_analyzer.detect_faces(frame)
        
        return {
            "status": "success",
            "faces": detections,
            "count": len(detections)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Detection error: {e}")
        return {
            "status": "error",
            "message": str(e),
            "faces": []
        }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🎯 SafeSight Vision Service")
    print("=" * 60)
    print(f"🌐 Host: {HOST}")
    print(f"🔌 Port: {PORT}")
    print(f"📡 Backend: {BACKEND_URL}")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )
