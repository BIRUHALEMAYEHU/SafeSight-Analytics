from fastapi import APIRouter
from app.api.api_v1.endpoints import cameras, persons

api_router = APIRouter()

api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(persons.router, prefix="/persons", tags=["persons"])
