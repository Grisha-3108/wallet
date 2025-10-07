from fastapi import APIRouter

from .v1.handlers import v1_router


api_main_router = APIRouter(prefix="/api")
api_main_router.include_router(v1_router)
