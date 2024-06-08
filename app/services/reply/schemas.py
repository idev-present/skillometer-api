from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class ReplyBase(BaseModel):
    vacancy_id: str
    applicant_id: Optional[str] = None
    owner_id: str


class ReplyInput(ReplyBase):
    pass


class ReplyInDB(ReplyBase):
    id: UUID
    status: str
    applicant_avatar: Optional[str] = None
    applicant_fullname: Optional[str] = None
    applicant_phone: Optional[str] = None
    applicant_telegram: Optional[str] = None
    applicant_email: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    updated_by: Optional[str]


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


# Reply status
class ReplyStatus(Enum):
    NEW = "NEW"
