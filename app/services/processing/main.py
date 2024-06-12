import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.services.applicant.db_models import ApplicantDBModel
from app.services.dict.const import REPLY_STATUS
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply
from app.services.user.db_models import UserDBModel
from app.services.vacancy.db_models import VacancyDBModel


async def create_reply(user_id: str, vacancy_id: str, applicant_id: str, db: Session):
    user = await UserDBModel.get(item_id=user_id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User #{user_id} not found")
    vacancy = await VacancyDBModel.get(item_id=vacancy_id, db=db)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Vacancy #{vacancy_id} not found")
    applicant = await ApplicantDBModel.get(item_id=applicant_id, db=db)
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
    reply = await ReplyDBModel.create(form=reply_form, db=db)
    return reply