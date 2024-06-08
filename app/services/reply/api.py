from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply

router = APIRouter()


@router.get("/")
async def reply_list(db_session=Depends(db_service.get_db)) -> List[Reply]:
    res = await ReplyDBModel.get_list(db_session)
    return res
