from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

from app.services.dict.const import CURRENCY


class Vacancy(BaseModel):
    id: str
    name: str
    habr_id: Optional[int] = None
    hh_id: Optional[int] = None
    url: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: dict = Field(..., pre=True)
    is_remote: bool = False
    description: str
    team: str
    todo: str
    city_id: Optional[str] = None
    employment_type_id: Optional[str] = None
    division_id: Optional[str] = None
    qualification_id: Optional[str] = None
    skill_set: Optional[str] = None
    created_at: Optional[datetime]
    published_at: Optional[datetime]
    owner_id: Optional[str] = None
    company_id: Optional[str] = None

    @field_validator("currency", mode="before")
    @classmethod
    def transform_currency(cls, v):
        # todo: check valid key
        for key in CURRENCY:
            if key.name == v:
                return {"key": key.name, "value": key.value}
        return v
