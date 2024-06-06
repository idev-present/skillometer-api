from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from app.core.db import db

api = APIRouter()


@api.get("/")
async def test(db_session=Depends(db.get_db)):
    try:
        await db_session.execute(text("SELECT 1"))
        return {"data": "ok"}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
