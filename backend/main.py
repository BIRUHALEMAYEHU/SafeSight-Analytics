"""
SafeSight Analytics - Backend API
FastAPI REST API for the SafeSight Analytics system
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SafeSight Analytics API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}

