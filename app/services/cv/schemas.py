from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.services.applicant.schemas import ApplicantXP, ApplicantEducation


class CV(BaseModel):
    id: str  # id из базы
    login: str  # slug
    avatar: Optional[str]  # avatar
    phone: Optional[str]  # Моб
    email: Optional[str]  # email
    bio: Optional[str]  # О себе
    gender: Optional[str]  # О себе
    salary_from: Optional[int]  # ЗП
    currency: Optional[str]  # валюта
    is_relocation: Optional[bool]  # готов к переезду
    is_remote: Optional[bool]  # готов к удаленке
    search_status_id: Optional[str]  # статус поиска
    qualification_id: Optional[str]  # квалификация
    division_id: Optional[str]  # специализация
    city_id: Optional[str]  # город
    skill_set: Optional[str]  # навыки
    experience: Optional[str]  # опыт работы
    age: Optional[int]  # возраст
    title: Optional[str]  # Имя фамилия
    registered_at: Optional[datetime]  # дата регистрации
    last_visited: Optional[datetime]  # дата последнего визита
    xp: List[ApplicantXP]  # опыт работы
    education: List[ApplicantEducation]  # образование