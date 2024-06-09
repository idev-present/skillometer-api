from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BaseUser(BaseModel):
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]


class UserInDB(BaseUser):
    id: str
    role: Optional[str] = Field(None)
    avatar: Optional[str]
    created_time: datetime = Field(alias='createdTime')


class UserSession(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
