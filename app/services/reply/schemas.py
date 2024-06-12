from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional


class ReplyForm(BaseModel):
    vacancy_id: str = Field(..., title="Vacancy ID")
    applicant_id: str = Field(..., title="Applicant ID")
    owner_id: Optional[str] = Field(None, title="Recruiter User ID")


class Reply(ReplyForm):
    id: UUID
    status: str
    applicant_avatar: Optional[str] = None
    applicant_fullname: Optional[str] = None
    applicant_phone: Optional[str] = None
    applicant_telegram: Optional[str] = None
    applicant_email: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    updated_by: Optional[str]
    updated_by_role: Optional[str]


class ReplyUpdateForm(BaseModel):
    status: str


# Reply comments
class ReplyCommentBase(BaseModel):
    author_id: str
    author_name: str
    reply_id: str
    content: str


class ReplyCommentInput(ReplyCommentBase):
    pass


class ReplyCommentInDB(ReplyCommentBase):
    id: UUID
    created_at: datetime
