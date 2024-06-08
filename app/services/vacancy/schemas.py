from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

from app.services.dict.const import CURRENCY
from app.services.dict.schemas import Currency


class VacancyForm(BaseModel):
    # * Config
    name: str
    salary_from: Optional[int] = Field(None)
    salary_to: Optional[int] = Field(None)
    # TODO: add enum
    currency: Optional[str] = Field(CURRENCY.RUR.name)
    is_remote: bool = False
    # * Description parts
    description: str
    team: str
    todo: str
    # * Dict
    # Город проживания
    city_id: str = Field(...)
    # Тип занятости
    employment_type_id: str = Field(...)
    # специализация
    division_id: str = Field(...)
    # Квалификация
    qualification_id: str = Field(...)
    # Навыки (от 1 до 10)
    skill_set: str = Field(...)


class VacancyListItem(VacancyForm):
    model_config = ConfigDict(from_attributes=True)

    id: str
    # * External links
    habr_id: Optional[int] = Field(None)
    hh_id: Optional[int] = Field(None)
    url: Optional[str] = Field(None)
    # * Config
    currency: Currency = Field(..., pre=True)
    # * Dict
    # * Timestamps
    created_at: Optional[datetime]
    published_at: Optional[datetime]
    # * Relationships
    owner_id: Optional[str] = Field(None)
    company_id: Optional[str] = Field(None)

    @field_validator("currency", mode="before")
    @classmethod
    def transform_currency(cls, v):
        # todo: check valid key
        for key in CURRENCY:
            if key.name == v:
                return Currency(key=key.name, value=key.value)
        return v


class Vacancy(VacancyForm):
    model_config = ConfigDict(from_attributes=True)

    id: str
    # * External links
    habr_id: Optional[int] = Field(None)
    hh_id: Optional[int] = Field(None)
    url: Optional[str] = Field(None)
    # * Config
    currency: Currency = Field(..., pre=True)
    # * Dict
    # * Timestamps
    created_at: Optional[datetime]
    published_at: Optional[datetime]
    # * Relationships
    owner_id: Optional[str] = Field(None)
    company_id: Optional[str] = Field(None)

    @field_validator("currency", mode="before")
    @classmethod
    def transform_currency(cls, v):
        # todo: check valid key
        for key in CURRENCY:
            if key.name == v:
                return Currency(key=key.name, value=key.value)
        return v


class VacancyUpdateForm(VacancyForm):
    name: Optional[str] = Field(None)
    is_remote: Optional[bool] = Field(False)
    description: Optional[str] = Field(None)
    team: Optional[str] = Field(None)
    todo: Optional[str] = Field(None)
    city_id: Optional[str] = Field(None)
    employment_type_id: Optional[str] = Field(None)
    division_id: Optional[str] = Field(None)
    qualification_id: Optional[str] = Field(None)
    skill_set: Optional[str] = Field(None)
