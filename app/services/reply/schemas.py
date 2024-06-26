from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional

from app.services.processing.schemas import MatchingResult


class ReplyForm(BaseModel):
    vacancy_id: str = Field(..., description="ID Вакансии")
    applicant_id: str = Field(..., description="ID Соискателя")
    owner_id: Optional[str] = Field(None, description="ID Рекрутера")
    chat_id: Optional[str] = Field(None, description='ID чата')
    user_comment: Optional[str] = Field(None, description='Комментарий соискателя')


class Reply(ReplyForm):
    id: UUID
    status: str
    reason: Optional[str] = Field(None, description="Причина изменения статуса")
    vacancy_name: Optional[str] = Field(None, description="Название вакансии")
    applicant_avatar: Optional[str] = None
    applicant_fullname: Optional[str] = None
    applicant_phone: Optional[str] = None
    applicant_telegram: Optional[str] = None
    applicant_email: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    updated_by_role: Optional[str]
    matching_result: Optional[MatchingResult] = Field(None, description="Результат сравнения по скиллам")


class ReplyUpdateForm(BaseModel):
    status: str
    reason: Optional[str] = Field(None, description="Причина изменения статуса")


class ReplyDBModelFilters(BaseModel):
    applicant_id: Optional[str] = None
    vacancy_id: Optional[str] = None
    status: Optional[str] = None


# Reply comments
class ReplyCommentBase(BaseModel):
    author_id: str
    author_name: str
    content: str


class ReplyCommentForm(ReplyCommentBase):
    pass


class ReplyCommentInDB(ReplyCommentBase):
    id: UUID
    reply_id: UUID
    created_at: datetime
