from fastapi import APIRouter
from app.api.api_v1.endpoints import cameras, persons, auth, alerts_ws

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(alerts_ws.router, prefix="/alerts", tags=["alerts"])
