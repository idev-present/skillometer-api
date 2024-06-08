from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Applicant(BaseModel):
    id: str
    user_id: str
    title: str
    salary_from: Optional[int]
    currency: Optional[str]
    age: Optional[int]
    experience: Optional[str]
    is_relocation: bool = False
    is_remote: bool = False
    last_visited: Optional[datetime]
    registered_at: Optional[datetime]
    search_status_id: Optional[str]
    qualification_id: Optional[str]
    division_id: Optional[str]
    city_id: Optional[str]
    skill_set: Optional[str]