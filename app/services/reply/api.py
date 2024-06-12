from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.processing.main import get_status_info, update_reply_status
from app.services.processing.schemas import ReplyStatusFlow
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply

router = APIRouter()


@router.get("/")
async def reply_list(db_session=Depends(db_service.get_db)) -> List[Reply]:
    res = await ReplyDBModel.get_list(db_session)
    return res


@router.get("/{reply_id}/status", response_model=List[ReplyStatusFlow])
async def get_reply_status_info(reply_id: str, db_session=Depends(db_service.get_db)):
    res = await get_status_info(reply_id=reply_id, db=db_session)
    return res


@router.post("/{reply_id}/status")
async def set_reply_status(reply_id: str, status: str, db_session=Depends(db_service.get_db)):
    res = await update_reply_status(reply_id=reply_id, to_status=status, db=db_session)
    return res