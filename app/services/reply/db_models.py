import sqlalchemy
from typing import List

from sqlalchemy import Column, String, DateTime, func, UUID
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.services.dict.const import REPLY_STATUS
from app.services.reply.schemas import Reply


class ReplyDBModel(BaseDBModel):
    __tablename__ = 'replies'

    id = Column(UUID, primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    status = Column(String, nullable=False, default=REPLY_STATUS.NEW.value)
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
    owner_id = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)
    updated_by_role = Column(String, nullable=True)
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
    async def create(cls, form: Reply, db) -> "ReplyDBModel":
        new_reply = cls(**form.dict())
        db.add(new_reply)
        await db.commit()
        await db.refresh(new_reply)
        return new_reply


class ReplyCommentDBModel(BaseDBModel):
    __tablename__ = 'replies_comments'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    author_id = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
    reply_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
