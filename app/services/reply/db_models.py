import sqlalchemy
from typing import List

from sqlalchemy import Column, String, DateTime, func, UUID
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel


class ReplyDBModel(BaseDBModel):
    __tablename__ = 'replies'

    id = Column(UUID, primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    status = Column(String, nullable=False)
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
    updated_by = Column(String, nullable=False)
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @classmethod
    async def get_list(cls, db) -> List["ReplyDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res


class ReplyCommentDBModel(BaseDBModel):
    __tablename__ = 'replies_comments'

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    author_id = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
    reply_id = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
