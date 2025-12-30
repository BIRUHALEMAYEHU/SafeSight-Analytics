"""
SafeSight Analytics - Backend API
FastAPI REST API for the SafeSight Analytics system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.camera import VideoCamera 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException
from app.db.session import get_db
from app.models.camera import Camera as CameraModel
from fastapi.staticfiles import StaticFiles
#from app.api.api_v1.api import api_router
import asyncio
import os

app = FastAPI(
    title="SafeSight Analytics API",
    description="Backend API for SafeSight Analytics video surveillance system",
    version="0.1.0"
)

# Configure CORS to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")


#app.include_router(api_router, prefix="/api/v1")



# gen_camera = VideoCamera() # Removed global instance



async def gen(camera):
    try:
        while True:
            # 1. Add a tiny delay to control FPS (e.g., 0.05 = 20 FPS)
            # This prevents "socket overflow"
            await asyncio.sleep(0.05) 
            frame = await camera.get_frame()
            if frame is None:
                break
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                   
    except Exception as e:
        # This catches "Connection closed by client" or "Broken pipe"
        print(f"Streaming connection ended: {e}")
    finally:
        camera.stop()
        print("Cleaning up video stream resources...")



@app.get("/video_feed")
async def video_feed(
    camera_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Stream video from a specific camera.
    If camera_id is not provided, defaults to local webcam (0).
    """
    source = 0 # Default to local webcam
    
    if camera_id:
        result = await db.execute(select(CameraModel).where(CameraModel.id == camera_id))
        camera_db = result.scalars().first()
        if not camera_db:
             raise HTTPException(status_code=404, detail="Camera not found")
        
        # Check if rtsp_url is an integer (webcam index) or string
        if camera_db.rtsp_url and camera_db.rtsp_url.isdigit():
             source = int(camera_db.rtsp_url)
        elif camera_db.rtsp_url:
             source = camera_db.rtsp_url
    
    # Instantiate camera for this stream
    # Note: For production, this needs a pool manager to avoid opening multiple connections to same camera
    camera = VideoCamera(source=source)
    
    return StreamingResponse(gen(camera), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SafeSight Analytics API",
        "version": "0.1.0",
        "status": "running"
    }

