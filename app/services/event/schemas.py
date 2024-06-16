from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class EVENT_STATUS(Enum):
    PLANNING = 'PLANNING'
    CONFIRMED = 'CONFIRMED'
    WAITING = 'WAITING'
    DONE = 'DONE'


class EVENT_TYPE(Enum):
    ZOOM = 'ZOOM'
    GOOGLE_MEET = 'GOOGLE_MEET'
    TELEGRAM = 'TELEGRAM'
    PHONE = 'PHONE'


class EventForm(BaseModel):
    type: EVENT_TYPE = Field(..., description="тип события: ZOOM, GOOGLE_MEET, TELEGRAM, PHONE")
    payload: Optional[str] = Field(None, description="Ссылка, номер телефона и другие дополнительные данные")
    name: Optional[str] = Field(None, description="название события")
    description: Optional[str] = Field(None, description="Описание события")
    start_at: Optional[datetime] = Field(None, description="дата и время начала события")
    end_at: Optional[datetime] = Field(None, description="дата и время окончания события")


class EventUpdateForm(EventForm):
    status: EVENT_STATUS = Field(..., description="статус события: PLANNING, CONFIRMED, WAITING, DONE")


class EventInput(EventForm):
    status: EVENT_STATUS = Field(..., description="статус события: PLANNING, CONFIRMED, WAITING, DONE")
    owner_id: UUID = Field(..., description="идентификатор владельца (рекрутера)")
    to_id: UUID = Field(..., description="идентификатор получателя (соискателя)")
    reply_id: UUID = Field(..., description="идентификатор ответившего пользователя")


class Event(EventForm):
    id: UUID = Field(...)
    status: EVENT_STATUS = Field(..., description="статус события: PLANNING, CONFIRMED, WAITING, DONE")
    is_deleted: Optional[bool] = Field(False, description="пометка об удалении события")
    created_at: datetime = Field(..., description="дата и время создания записи")
    updated_at: Optional[datetime] = Field(None, description="дата и время последнего обновления записи")
    updated_by: Optional[UUID] = Field(None, description="идентификатор последнего обновившего пользователя")
