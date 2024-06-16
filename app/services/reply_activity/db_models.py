from typing import List

import uuid
from sqlalchemy import Column, UUID, String, Text, ForeignKey, DateTime, func, sql
from sqlalchemy.orm import joinedload, relationship

from app.core.db import BaseDBModel
from app.services.reply_activity.schemas import ReplyActivityForm


class ActivityDBModel(BaseDBModel):
    __tablename__ = 'reply_activity'

    id = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(50), nullable=False)  # REPLY_STATUS | EVENT_STATUS
    text = Column(Text, nullable=True)
    external_id = Column(String(50), nullable=True)  # reply_id | event_id
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    owner_type = Column(String(50), nullable=True)  # user.role
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("UserDBModel")

    @classmethod
    def create(cls, form: ReplyActivityForm, db) -> "ActivityDBModel":
        new_event = cls(**form.dict())
        new_event.id = uuid.uuid4()
        new_event.type = form.type.value
        db.add(new_event)
        db.commit()
        db.refresh(new_event)
        return new_event

    @classmethod
    def get_list(cls, db, reply_id: str) -> List["ActivityDBModel"]:
        query = sql.select(cls).options(joinedload(cls.user)).filter(cls.external_id == reply_id)
        result = db.execute(query)
        return result.scalars().all()
