from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Vacancy(BaseModel):
    id: str
    habr_id: Optional[int] = None
    hh_id: Optional[int] = None
    url: Optional[str] = None
    salary_from: Optional[int] = None
    salary_to: Optional[int] = None
    currency: str
    is_remote: bool = False
    description: str
    team: str
    todo: str
    city_id: Optional[str] = None
    employment_type_id: Optional[str] = None
    division_id: Optional[str] = None
    qualification_id: Optional[str] = None
    skills: Optional[str] = None
    created_at: datetime
    published_at: datetime
    owner_id: Optional[str] = None
    company_id: Optional[str] = None