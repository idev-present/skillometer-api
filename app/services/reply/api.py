from typing import List, Optional

from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status

from app.core.db import db_service
from app.core.iam.schemas import TokenData
from app.services.dict.schemas import ReplyStatusCount
from app.services.reply.db_models import ReplyDBModel, ReplyCommentDBModel
from app.services.reply.schemas import Reply, ReplyCommentForm, ReplyCommentInDB, ReplyUpdateForm, ReplyDBModelFilters
from app.services.processing.main import get_status_info, update_reply_status, calculate_matching
from app.services.processing.schemas import ReplyStatusFlow
from app.services.reply_activity.db_models import ActivityDBModel
from app.services.reply_activity.schemas import ReplyActivity
from app.services.user.middlewares import get_current_user
from app.services.vacancy.db_models import VacancyDBModel

router = APIRouter()


@router.get("/", response_model=List[Reply])
def reply_list(
        applicant_id: Optional[str] = None,
        vacancy_id: Optional[str] = None,
        status: Optional[str] = None,
        db_session=Depends(db_service.get_db)
):
    filters = ReplyDBModelFilters(
        applicant_id=applicant_id,
        vacancy_id=vacancy_id,
        status=status,
    )
    reply_list_result = ReplyDBModel.get_list(db=db_session, filters=filters)
    res = []
    if vacancy_id and status:
        vacancy = VacancyDBModel.get(db=db_session, item_id=vacancy_id)
        for reply in reply_list_result:
            model = Reply.model_validate(reply.__dict__)
            matching_result = calculate_matching(db=db_session, reply=reply, vacancy=vacancy)
            if matching_result:
                model.matching_result = matching_result
            res.append(model)
    else:
        res = reply_list_result
    return res


@router.get("/{reply_id}", response_model=Reply)
def get_reply(reply_id: str, db_session=Depends(db_service.get_db)):
    res = ReplyDBModel.get(item_id=reply_id, db=db_session)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reply not found")
    return res


@router.get("/{reply_id}/matching")
def get_reply_matching(reply_id: str, db_session=Depends(db_service.get_db)):
    reply = ReplyDBModel.get(db=db_session, item_id=reply_id)
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reply not found")
    vacancy = VacancyDBModel.get(db=db_session, item_id=reply.vacancy_id)
    res = calculate_matching(reply=reply, vacancy=vacancy, db=db_session)
    return res


@router.get("/{reply_id}/status", response_model=List[ReplyStatusFlow])
def get_reply_next_status_flow(reply_id: str, db_session=Depends(db_service.get_db)):
    res = get_status_info(reply_id=reply_id, db=db_session)
    return res


@router.post("/{reply_id}/status")
def set_reply_status(
        reply_id: str, form: ReplyUpdateForm,
        token_data: TokenData = Depends(get_current_user),
        db_session=Depends(db_service.get_db)
):
    set_by = token_data.id
    res = update_reply_status(
        reply_id=reply_id,
        to_status=form.status,
        reason=form.reason,
        user_id=set_by,
        db=db_session
    )
    return res


@router.post("/{reply_id}/comments", response_model=List[ReplyCommentInDB])
def reply_comment_create(
        reply_id: str,
        comment: ReplyCommentForm,
        db_session=Depends(db_service.get_db)
) -> List[ReplyCommentInDB]:
    res = ReplyCommentDBModel.create(reply_id, comment, db=db_session)
    return res


@router.get("/{reply_id}/comments", response_model=List[ReplyCommentInDB])
def get_reply_comments(reply_id: str, db_session=Depends(db_service.get_db)) -> List[ReplyCommentInDB]:
    res = ReplyCommentDBModel.get_list(reply_id, db=db_session)
    return res


@router.get("/{reply_id}/activity", response_model=List[ReplyActivity])
def get_reply_activity(reply_id: str, db_session=Depends(db_service.get_db)) -> List[ReplyActivity]:
    res = ActivityDBModel.get_list(reply_id=reply_id, db=db_session)
    return res


@router.get("/{vacancy_id}/count", response_model=List[ReplyStatusCount])
def reply_count_by_status(vacancy_id: str, db_session=Depends(db_service.get_db)):
    return ReplyDBModel.count_by_vacancy(vacancy_id=vacancy_id, db=db_session)
