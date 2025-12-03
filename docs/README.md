# SafeSight Analytics Documentation

This directory contains documentation for the SafeSight Analytics project.

## Overview

SafeSight Analytics is a real-time video surveillance system that performs:
- Face detection and recognition
- Object detection for high-risk items
- Behavior/condition rule-based alerting
- Web-based control panel for operators

## Architecture

The system consists of three main components:

1. **Backend** (`/backend`): FastAPI REST API that handles API requests and coordinates between services
2. **Frontend** (`/frontend`): React-based web dashboard for viewing alerts and managing the system
3. **Vision** (`/vision`): Python service that handles camera input and performs video analysis

## API Documentation

API documentation will be available at `http://localhost:8000/docs` when the backend is running (FastAPI automatic docs).

## Development Notes

- The vision service currently only reads frames; ML models will be added in future iterations
- Database integration is planned but not yet implemented
- Camera access may require additional permissions on some systems

