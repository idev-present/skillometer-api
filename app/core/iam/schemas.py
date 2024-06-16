from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from typing import Optional, List, Dict, Literal

from app.utils.api_utils import str2datetime


class TokenData(BaseModel):
    id: str = Field(...)
    email: str = Field(...)
    name: Optional[str] = None
    displayName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    emailVerified: Optional[bool] = None
    phone: Optional[str] = None
    avatar: Optional[str] = None
    permanentAvatar: Optional[str] = None
    isDefaultAvatar: Optional[bool] = None
    owner: Optional[str] = None
    signupApplication: Optional[str] = None
    type: Optional[str] = None
    roles: Optional[List[Dict]] = None
    permissions: Optional[List[str]] = None
    tag: Optional[str] = None
    isOnline: Optional[bool] = None
    isAdmin: Optional[bool] = None
    isForbidden: Optional[bool] = None
    isDeleted: Optional[bool] = None
    createdTime: Optional[datetime] = None
    updatedTime: Optional[datetime] = None

    @field_validator('createdTime', 'updatedTime', mode="before")
    @classmethod
    def parse_datetime(cls, v):
        if isinstance(v, str):
            return str2datetime(v)
        return v


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


# * User
class IAMUser(BaseModel):
    id: str = Field(...)
    name: Optional[str] = Field(None)
    avatar: Optional[str] = Field(None)
    gender: Optional[Literal['male', 'female']] = Field(None)
    firstName: Optional[str] = Field(None)
    lastName: Optional[str] = Field(None)
    birthday: Optional[datetime] = Field(None)
    bio: Optional[str] = Field(None, title="О себе", description="text/html")
    role: Optional[Literal['applicant', 'recruiter']] = Field(None)
    displayName: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    emailVerified: Optional[bool] = Field(None)
    phone: Optional[str] = Field(None)
    countryCode: Optional[str] = Field(None)
    location: Optional[str] = Field(None)
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)
    deleted_at: Optional[datetime] = Field(None)

    @model_validator(mode="before")
    @classmethod
    def prepare_user_fields(cls, data: Dict) -> Dict:
        cls.prepare_user_role(data)
        cls.prepare_fullname(data)
        cls.prepare_gender(data)
        cls.prepare_time_fields(data, ['birthday', 'createdTime', 'updatedTime', 'deletedTime'])
        return data

    @staticmethod
    def prepare_fullname(data: Dict):
        if data.get('displayName'):
            name_parts = data['displayName'].split(' ')
            if len(name_parts) == 1:
                data['firstName'] = name_parts[0]
            else:
                if not data.get('firstName'):
                    data['firstName'] = name_parts[1]
                if not data.get('lastName'):
                    data['lastName'] = name_parts[0]

    @staticmethod
    def prepare_user_role(data: Dict):
        if 'tag' in data and data.get('tag'):
            data['role'] = 'recruiter' if data.get('tag') == 'recruiter_tag' else 'applicant'
        else:
            data['role'] = 'applicant'

    @staticmethod
    def prepare_gender(data: Dict):
        if 'gender' in data and data['gender'] == '':
                data['gender'] = None

    @staticmethod
    def prepare_time_fields(data: Dict, time_fields: List[str]):
        for field in time_fields:
            if field in data:
                field_name = f"{field.replace('Time', '')}_at" if field != 'birthday' else field
                if data.get(field) == "":
                    data[field] = None
                    data[field_name] = None
                else:
                    data[field_name] = str2datetime(data[field])
