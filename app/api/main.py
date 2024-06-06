from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.dict.api import router as dict_router

api = APIRouter()
api.include_router(dict_router, prefix="/dict", tags=["dict"])


@api.get("/config")
async def show_settings():
    try:
        return settings
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
