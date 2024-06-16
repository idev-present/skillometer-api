import uuid
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.services.applicant.db_models import ApplicantDBModel
from app.services.chat.api import send_message
from app.services.chat.const import CHAT_ROOM_TYPE, MESSAGE_TYPE, MESSAGE_STATUS
from app.services.chat.db_models import ChatRoomDBModel, MessageDBModel
from app.services.chat.schemas import ChatRoomForm, MessageForm
from app.services.dict.const import REPLY_STATUS
from app.services.processing.status_mapper import available_status_flow
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply, ReplyUpdateForm
from app.services.user.db_models import UserDBModel
from app.services.vacancy.db_models import VacancyDBModel


def create_reply(user_id: str, vacancy_id: str, applicant_id: str, comment: Optional[str], db: Session):
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
        vacancy_name=vacancy.name,
        applicant_id=applicant.id,
        applicant_avatar=user.avatar,
        applicant_fullname=applicant.title,
        applicant_phone=user.phone,
        applicant_email=user.email,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        updated_by=str(user.id),
        updated_by_role=user.role,
        user_comment=comment
    )
    reply = ReplyDBModel.create(form=reply_form, db=db)
    if reply:
        # Создание чата
        chat_form = ChatRoomForm(
            name=reply.vacancy_name,
            type=CHAT_ROOM_TYPE.REPLY,
            reply_id=reply.id,
            applicant_id=applicant.user_id,
            recruiter_id=vacancy.owner_id,
            unread_count=1
        )
        created_chat = ChatRoomDBModel.create(form=chat_form, db=db)
        if created_chat:
            # Отправка первого сообщения в чат
            reply.chat_id = created_chat.id
            chat_message_form = MessageForm(
                type=MESSAGE_TYPE.TEXT.name,
                content=reply.user_comment,
                status=MESSAGE_STATUS.SENT.name,
                from_id=created_chat.applicant_id,
                to_id=created_chat.recruiter_id,
                room_id=created_chat.id,
            )
            MessageDBModel.create(form=chat_message_form, db=db)
        db.commit()
        db.refresh(reply)
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


def calculate_matching(reply: ReplyDBModel, db: Session, vacancy: Optional[VacancyDBModel] = None, applicant: Optional[ApplicantDBModel] = None):
    if not vacancy:
        vacancy = VacancyDBModel.get(item_id=reply.vacancy_id, db=db)
    if not applicant:
        applicant = ApplicantDBModel.get(item_id=reply.applicant_id, db=db)

    vacancy_skillset = set([skill for skill in vacancy.skill_set.split(',')])
    applicant_skillset = set([skill for skill in applicant.skill_set.split(',')])

    missed_skills = vacancy_skillset.difference(applicant_skillset)
    additional_skills = applicant_skillset.difference(vacancy_skillset)
    return {
        "missed_skills": missed_skills,
        "additional_skills": additional_skills,
        "coverage": (len(vacancy_skillset) - len(missed_skills)) / len(vacancy_skillset)
    }