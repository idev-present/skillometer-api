import sqlalchemy
from typing import List, Optional

from sqlalchemy import Column, String, DateTime, func, UUID
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.services.dict.const import REPLY_STATUS
from app.services.reply.schemas import Reply, ReplyUpdateForm, ReplyDBModelFilters, ReplyCommentForm


class ReplyDBModel(BaseDBModel):
    __tablename__ = 'replies'

    id = Column(UUID, primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"))
    status = Column(String, nullable=False, default=REPLY_STATUS.NEW.value)
    reason = Column(String, nullable=True)
    # Vacancy
    vacancy_id = Column(String, nullable=False)
    vacancy_name = Column(String, nullable=True)
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
    def create(cls, form: Reply, db) -> "ReplyDBModel":
        new_reply = cls(**form.dict())
        db.add(new_reply)
        db.commit()
        db.refresh(new_reply)
        return new_reply

    @classmethod
    def get(cls, db, item_id: str) -> "ReplyDBModel":
        query = sql.select(cls).filter(cls.id == item_id)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def update(cls, db, item_id: str, form: ReplyUpdateForm) -> "ReplyDBModel":
        reply = cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(reply, field, value)
        db.add(reply)
        db.commit()
        db.refresh(reply)
        return reply

    @classmethod
    def get_list(cls, db, filters: Optional[ReplyDBModelFilters] = None) -> List["ReplyDBModel"]:
        query = sql.select(cls)
        if filters:
            if filters.applicant_id:
                query = query.where(cls.applicant_id == filters.applicant_id)
        res = db.execute(query)
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

    @classmethod
    def get_list(cls, reply_id: str, db) -> List["ReplyCommentDBModel"]:
        query = sql.select(cls).filter(cls.reply_id == reply_id).order_by(cls.created_at.desc())
        result = db.execute(query)
        result = result.scalars().all()
        return result

    @classmethod
    def create(cls, reply_id: str, form: ReplyCommentForm, db) -> List["ReplyCommentDBModel"]:
        reply_comment = cls(**form.dict())
        reply_comment.reply_id = reply_id
        db.add(reply_comment)
        db.commit()
        db.refresh(reply_comment)
        return cls.get_list(reply_id, db)
