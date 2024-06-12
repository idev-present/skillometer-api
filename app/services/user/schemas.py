from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional, Literal


class UserForm(BaseModel):
    login: str = Field(..., description="Username used to log in")
    avatar: Optional[str] = Field(None, description="A link to the user's avatar picture")
    gender: Optional[Literal["male", "female"]] = Field(None, description="The user's gender")
    first_name: str = Field(None, description="The user's first name")
    last_name: str = Field(None, description="The user's last name")
    birthday: Optional[datetime] = Field(None, description="The user's birthday")
    city: Optional[str] = Field(None, description="The user's hometown or current city of residence")
    bio: Optional[str] = Field(None, description="A short description or biography of the user")


class User(UserForm):
    id: UUID = Field(..., description="The unique identifier for the user")
    first_name: Optional[str] = Field(None, description="The user's first name")
    last_name: Optional[str] = Field(None, description="The user's last name")
    full_name: str = Field(..., description="The user's full name")
    role: str = Field(..., description="The user's role in the system")
    email: str = Field(..., description="The user's email address")
    country_code: str = Field("RU", description="The user's country code")
    phone: Optional[str] = Field(None, description="The user's phone number")
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)
    deleted_at: Optional[datetime] = Field(None)


class UserUpdateForm(UserForm):
    login: Optional[str] = Field(None, description="Username used to log in")
    first_name: Optional[str] = Field(None, description="The user's first name")
    last_name: Optional[str] = Field(None, description="The user's last name")
