import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.services.applicant.db_models import ApplicantDBModel
from app.services.dict.const import REPLY_STATUS
from app.services.processing.status_mapper import available_status_flow
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply, ReplyUpdateForm
from app.services.user.db_models import UserDBModel
from app.services.vacancy.db_models import VacancyDBModel


def create_reply(user_id: str, vacancy_id: str, applicant_id: str, db: Session):
    user = UserDBModel.get(item_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User #{user_id} not found")
    vacancy = VacancyDBModel.get(item_id=vacancy_id, db=db)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Vacancy #{vacancy_id} not found")
    applicant = ApplicantDBModel.get(item_id=applicant_id, db=db)
    if not applicant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Applicant #{applicant_id} not found")
    reply_form = Reply(
        id=str(uuid.uuid4()),
        status=REPLY_STATUS.NEW.name,
        vacancy_id=vacancy.id,
        applicant_id=applicant.id,
        applicant_avatar=user.avatar,
        applicant_fullname=applicant.title,
        applicant_phone=user.phone,
        applicant_email=user.email,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        updated_by=str(user.id),
        updated_by_role=user.role
    )
    reply = ReplyDBModel.create(form=reply_form, db=db)
    return reply


def get_status_info(reply_id: str, db: Session):
    reply = ReplyDBModel.get(item_id=reply_id, db=db)
    available_flows = available_status_flow.get(reply.status)
    if not available_flows:
        return []
    return available_flows


def update_reply_status(reply_id: str, to_status: str, reason: Optional[str], db: Session):
    available_flow = get_status_info(reply_id=reply_id, db=db)
    available_status_list = [item.status for item in available_flow]
    if to_status not in available_status_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Status #{reply_id} not available")
    available_flow_item = available_flow[available_status_list.index(to_status)]
    if available_flow_item.is_required_reason and not reason:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Reason for status #{to_status} is required")
    update_form = ReplyUpdateForm(status=to_status, reason=reason)
    updated_reply = ReplyDBModel.update(item_id=reply_id, form=update_form, db=db)
    new_available_flow = available_status_flow.get(updated_reply.status)
    if not new_available_flow:
        return []
    new_available_status_list = [item.status for item in new_available_flow]
    if not new_available_status_list:
        return []
    return new_available_status_list
