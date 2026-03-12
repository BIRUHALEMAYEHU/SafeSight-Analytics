from fastapi import APIRouter
from app.api.api_v1.endpoints import cameras, persons, auth, alerts_ws, events, rules, alerts

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(alerts_ws.router, prefix="/alerts-ws", tags=["alerts-websocket"])
