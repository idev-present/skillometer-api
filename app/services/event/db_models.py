import uuid
from typing import List

from sqlalchemy import Column, String, ForeignKey, UUID, Boolean, DateTime, func, sql, not_
from sqlalchemy.orm import mapped_column

from app.core.db import BaseDBModel
from app.services.event.schemas import EventInput, EventUpdateForm, EventFilters, EVENT_STATUS
from app.services.reply_activity.const import ACTIVITY_TYPE
from app.services.reply_activity.db_models import ActivityDBModel
from app.services.reply_activity.schemas import ReplyActivityForm


class EventDBModel(BaseDBModel):
    __tablename__ = 'events'

    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(50), nullable=False)  # ZOOM | GOOGLE_MEET | TELEGRAM | PHONE
    status = Column(String(50), nullable=False)  # PLANNING | CONFIRMED | WAITING |DONE
    payload = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # id рекрутера
    to_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # id соискателя
    reply_id = Column(UUID(as_uuid=True), ForeignKey('replies.id'), nullable=False)

    is_deleted = Column(Boolean(), default=False)
    start_at = Column(DateTime(timezone=True), nullable=True)  # Дата+время начала
    end_at = Column(DateTime(timezone=True), nullable=True)  # Дата+время завершения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), nullable=True)

    @classmethod
    def create(cls, db, form: EventInput) -> "EventDBModel":
        event = cls(**form.dict())
        event.id = uuid.uuid4()
        event.type = form.type.value
        event.status = form.status.value
        db.add(event)
        db.commit()
        db.refresh(event)
        if event:
            activity = ReplyActivityForm(
                type=ACTIVITY_TYPE.EVENT_STATUS,
                text=f'Создано новое событие: {event.name}',
                external_id=str(event.id),
                owner_id=event.owner_id,
                owner_type='recruiter'
            )
            ActivityDBModel.create(form=activity, db=db)
        return event

    @classmethod
    def get(cls, db, item_id: UUID) -> "EventDBModel":
        query = sql.select(cls).filter(cls.id == item_id)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def update(cls, db, item_id: UUID, form: EventUpdateForm) -> "EventDBModel":
        event = cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(event, field, value)
        if form.type:
            event.type = form.type.value
        if form.status:
            event.status = form.status.value
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @classmethod
    def delete(cls, db, item_id: UUID) -> bool:
        message = cls.get(db, item_id)
        db.delete(message)
        db.commit()
        return True

    @classmethod
    def get_list(cls, filters: EventFilters, db) -> List["EventDBModel"]:
        query = sql.select(cls)
        if filters.recruiter_id:
            query = query.where(cls.owner_id == filters.recruiter_id)
        if filters.applicant_id:
            query = query.where(cls.to_id == filters.applicant_id)
        if filters.status:
            query = query.where(cls.status == filters.status.name)
        if filters.start_date:
            query = query.where(cls.start_at >= filters.start_date)
        if filters.end_date:
            query = query.where(cls.end_at <= filters.end_date)
        else:
            query = query.where(not_(cls.status == EVENT_STATUS.DONE.value))
        res = db.execute(query)
        res = res.scalars().all()

        return res
