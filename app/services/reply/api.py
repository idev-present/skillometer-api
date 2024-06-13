from typing import List, Optional

from fastapi import APIRouter, Depends, Body

from app.core.db import db_service
from app.services.processing.main import get_status_info, update_reply_status
from app.services.processing.schemas import ReplyStatusFlow
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply, ReplyUpdateForm

router = APIRouter()


@router.get("/")
async def reply_list(db_session=Depends(db_service.get_db)) -> List[Reply]:
    res = await ReplyDBModel.get_list(db=db_session)
    return res


@router.get("/{reply_id}/status", response_model=List[ReplyStatusFlow])
async def get_reply_next_status_flow(reply_id: str, db_session=Depends(db_service.get_db)):
    res = await get_status_info(reply_id=reply_id, db=db_session)
    return res


@router.post("/{reply_id}/status")
async def set_reply_status(reply_id: str, form: ReplyUpdateForm, db_session=Depends(db_service.get_db)):
    res = await update_reply_status(reply_id=reply_id, to_status=form.status, reason=form.reason, db=db_session)
    return res