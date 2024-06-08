from pydantic import BaseModel
from typing import Optional


class Currency(BaseModel):
    key: str
    value: str


class City(BaseModel):
    fias_id: Optional[str]
    habr_id: Optional[int]
    habr_alias: Optional[str]
    name: Optional[str]
    country_name: Optional[str]
    region_name: Optional[str]


class EmploymentType(BaseModel):
    id: str
    name: Optional[str]
    habr_id: Optional[str]
    hh_id: Optional[str]


class Division(BaseModel):
    id: str
    name: Optional[str]
    habr_id: Optional[int]


class Qualification(BaseModel):
    id: str
    name: Optional[str]
    habr_id: Optional[int]


class SearchStatus(BaseModel):
    id: Optional[str]
    name: Optional[str]
    habr_id: Optional[int]


class Skill(BaseModel):
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]
    qualification_id: Optional[str]
    division_id: Optional[str]
    habr_id: Optional[int]