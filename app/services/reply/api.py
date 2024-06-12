from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.reply.db_models import ReplyDBModel, ReplyCommentDBModel
from app.services.reply.schemas import Reply, ReplyCommentForm, ReplyCommentInDB

router = APIRouter()


@router.get("/")
async def reply_list(db_session=Depends(db_service.get_db)) -> List[Reply]:
    res = await ReplyDBModel.get_list(db_session)
    return res

@router.post("/{reply_id}")
async def comment_create(
        reply_id: str,
        comment: ReplyCommentForm,
        db_session=Depends(db_service.get_db)
) -> List[ReplyCommentInDB]:
    res = await ReplyCommentDBModel.create(reply_id, comment, db_session)
    return res
