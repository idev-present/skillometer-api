from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

from app.services.dict.const import CURRENCY
from app.services.dict.schemas import Currency


class ApplicantForm(BaseModel):
    salary_from: int = Field(..., gt=0)
    currency: Optional[str] = Field(CURRENCY.RUR.name)
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
    last_visited: Optional[datetime] = Field(None, description="Дата/время последнего посещения")
    registered_at: Optional[datetime] = Field(None, description="Дата/время регистрации")
    # * Computed fields
    experience: Optional[str] = Field(None, description="Суммарный опыт работы, калькулируется из списка")
    age: int = Field(..., gt=0)
    title: str = Field(...)

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
    salary_from: Optional[int] = Field(None)


# * Job XP
class ApplicantXPForm(BaseModel):
    company_name: str = Field(..., title="Name of the company")
    company_id: Optional[str] = Field(None, title="The unique identifier of the company")
    position: str = Field(..., title="Position held at the company")
    position_id: Optional[str] = Field(None, title="The unique identifier of the position")
    start_date: datetime = Field(..., title="Start date of the position")
    end_date: Optional[datetime] = Field(None, title="End date of the position")
    description: Optional[str] = Field(None, title="Description of position and responsibilities")
    skill_set: Optional[str] = Field(None, title="Skills applied in the position")


class ApplicantXP(ApplicantXPForm):
    id: str = Field(..., title="The unique identifier of the experience")
    applicant_id: str = Field(..., title="The unique identifier of the applicant", max_length=50)


class ApplicantXPUpdateForm(ApplicantXPForm):
    company_name: Optional[str] = Field(None, title="Name of the company")
    position: Optional[str] = Field(None, title="Position held at the company")
    start_date: Optional[datetime] = Field(None, title="Start date of the position")
