from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.services.applicant.schemas import ApplicantXP, ApplicantEducation


class CV(BaseModel):
    login: str  # slug
    avatar: str  # avatar
    phone: str  # Моб
    email: str  # email
    bio: Optional[str]  # О себе
    id: str  # id из базы
    salary_from: int  # ЗП
    currency: str  # валюта
    is_relocation: bool  # готов к переезду
    is_remote: bool  # готов к удаленке
    search_status_id: str  # статус поиска
    qualification_id: Optional[str]  # квалификация
    division_id: Optional[str]  # специализация
    city_id: str  # город
    skill_set: str  # навыки
    experience: str  # опыт работы
    age: int  # возраст
    title: str  # Имя фамилия
    registered_at: Optional[datetime]  # дата регистрации
    last_visited: Optional[datetime]  # дата последнего визита
    xp: List[ApplicantXP]  # опыт работы
    education: List[ApplicantEducation]  # образование