from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

from app.services.dict.const import CURRENCY
from app.services.dict.schemas import Currency


class ApplicantForm(BaseModel):
    title: str = Field(...)
    salary_from: int = Field(..., gt=0)
    currency: Optional[str] = Field(CURRENCY.RUR.name)
    age: int = Field(..., gt=0)
    is_relocation: Optional[bool] = Field(False, description="Готовность к переезду")
    is_remote: Optional[bool] = Field(False, description="Готовность к удаленной работе")
    # * Dict
    search_status_id: Optional[str] = Field(None)
    qualification_id: Optional[str] = Field(None)
    division_id: Optional[str] = Field(None)
    city_id: Optional[str] = Field(None)
    skill_set: Optional[str] = Field(None)


class ApplicantListItem(ApplicantForm):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    # * Config
    currency: Currency = Field(...)
    experience: Optional[str] = Field(None, description="Суммарный опыт работы, калькулируется из списка")
    last_visited: Optional[datetime] = Field(None, description="Дата/время последнего посещения")
    registered_at: Optional[datetime] = Field(None, description="Дата/время регистрации")

    @field_validator("currency", mode="before")
    @classmethod
    def transform_currency(cls, v):
        # todo: check valid key
        for key in CURRENCY:
            if key.name == v:
                return Currency(key=key.name, value=key.value)
        return v


class Applicant(ApplicantListItem):
    pass


class ApplicantUpdateForm(ApplicantForm):
    title: Optional[str] = Field(None)
    salary_from: Optional[int] = Field(None)
    age: Optional[int] = Field(None)