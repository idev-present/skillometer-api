import sqlalchemy
from typing import List

from fastapi import HTTPException
from sqlalchemy import Column, String, DateTime, func, UUID, select
from sqlalchemy.sql import expression as sql
from starlette import status

from app.core.db import BaseDBModel
from app.services.applicant.db_models import ApplicantDBModel
from app.services.reply.schemas import ReplyStatus
from app.services.vacancy.db_models import VacancyDBModel


class ReplyDBModel(BaseDBModel):
    __tablename__ = 'replies'

    id = Column(UUID, primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    status = Column(String, nullable=False, default=ReplyStatus.NEW.value)
    # Vacancy
    vacancy_id = Column(String, nullable=False)
    # Applicant
    applicant_id = Column(String, nullable=True)
    applicant_avatar = Column(String, nullable=True)
    applicant_fullname = Column(String, nullable=True)
    applicant_phone = Column(String, nullable=True)
    applicant_telegram = Column(String, nullable=True)
    applicant_email = Column(String, nullable=True)
    # Owner
    owner_id = Column(String, nullable=False)
    updated_by = Column(String, nullable=True)
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    async def get_list(cls, db) -> List["ReplyDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res

    @classmethod
    async def create(cls, data, db_session):
        if data.vacancy_id:
            vacancy_db_model: VacancyDBModel = await db_session.execute(
                select(VacancyDBModel).where(VacancyDBModel.id == data.vacancy_id)).scalars().first()
            if not vacancy_db_model:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Vacancy #{data.vacancy_id} not found'
                )
        if data.applicant_id:
            applicant_db_model: ApplicantDBModel = await db_session.execute(
                select(ApplicantDBModel).where(ApplicantDBModel.id == data.applicant_id)).scalars().first()
            if not applicant_db_model:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Applicant #{data.applicant_id} not found'
                )
        new_reply = cls(**data.dict())
        # new_reply.owner_id = vacancy_db_model.owner_id
        # new_reply.applicant_phone = applicant_db_model.
        # new_reply.applicant_avatar = applicant_db_model.
        # new_reply.applicant_fullname = applicant_db_model.
        # new_reply.applicant_telegram = applicant_db_model.
        # new_reply.applicant_email = applicant_db_model.
        db_session.add(new_reply)
        await db_session.commit()
        await db_session.refresh(new_reply)
        return new_reply


class ReplyCommentDBModel(BaseDBModel):
    __tablename__ = 'replies_comments'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    author_id = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
    reply_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
