from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import ReplyInput, ReplyInDB
from app.services.vacancy.db_models import VacancyDBModel

router = APIRouter()


@router.get("/")
async def reply_list(db_session=Depends(db_service.get_db)) -> List[ReplyInDB]:
    res = await ReplyDBModel.get_list(db_session)
    return res


@router.post("/")
async def create(data: ReplyInput, db_session=Depends(db_service.get_db)) -> ReplyInDB:
    res = await ReplyDBModel.create(data, db_session)
    return res
