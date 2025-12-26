"""
SafeSight Analytics - Backend API
FastAPI REST API for the SafeSight Analytics system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from utils.camera import VideoCamera 
import asyncio

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

gen_camera = VideoCamera()



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
        print("Cleaning up video stream resources...")

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(gen(gen_camera), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SafeSight Analytics API",
        "version": "0.1.0",
        "status": "running"
    }

