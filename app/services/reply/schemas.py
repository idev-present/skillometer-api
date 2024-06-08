from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ReplyBase(BaseModel):
    status: str
    vacancy_id: str
    applicant_id: Optional[str] = None
    applicant_avatar: Optional[str] = None
    applicant_fullname: Optional[str] = None
    applicant_phone: Optional[str] = None
    applicant_telegram: Optional[str] = None
    applicant_email: Optional[str] = None
    owner_id: str
    updated_by: str


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyBase):
    id: str
    created_at: datetime
    updated_at: datetime


# Reply comments
class ReplyCommentBase(BaseModel):
    author_id: str
    author_name: str
    reply_id: str
    content: str


class ReplyCommentCreate(ReplyCommentBase):
    pass


class ReplyComment(ReplyCommentBase):
    id: str
    created_at: datetime


# Reply status
class ReplyStatus(BaseModel):
    pass
