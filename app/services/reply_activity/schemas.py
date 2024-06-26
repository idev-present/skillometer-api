from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional

from app.services.reply_activity.const import ACTIVITY_TYPE
from app.services.user.schemas import User


class ReplyActivityForm(BaseModel):
    type: Optional[ACTIVITY_TYPE] = Field(None, description='Тип события')
    text: Optional[str] = Field(None)
    external_id: str = Field(description='ID отклика или события')
    owner_id: Optional[UUID] = Field(description='ID пользователя')
    owner_type: Optional[str] = Field(description='Соискатель/рекрутер')


class ReplyActivity(ReplyActivityForm):
    id: UUID
    owner: Optional[User] = None
    created_at: Optional[datetime]
