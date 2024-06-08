from typing import List

from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel


class ApplicantDBModel(BaseDBModel):
    __tablename__ = 'applicants'

    id = Column(String, primary_key=True)
    user_id = Column(String(50), nullable=False)
    title = Column(String, nullable=False)
    salary_from = Column(Integer, nullable=True)
    currency = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    experience = Column(String)
    is_relocation = Column(Boolean, default=False)
    is_remote = Column(Boolean, default=False)
    last_visited = Column(DateTime, nullable=True)
    registered_at = Column(DateTime, nullable=True)
    # * Dict
    # статус поиска
    search_status_id = Column(String(50), nullable=True)
    # Квалификация
    qualification_id = Column(String(50), nullable=True)
    # специализация
    division_id = Column(String(50), nullable=True)
    # Город проживания
    city_id = Column(String(50), nullable=True)
    # Примененные навыки
    skill_set = Column(String, nullable=True)

    @classmethod
    async def get_list(cls, db) -> List["ApplicantDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res


class ApplicantXPDBModel(BaseDBModel):
    __tablename__ = 'applicant_xp'

    id = Column(String, primary_key=True)
    applicant_id = Column(String(50), nullable=False)
    # Компания
    company_name = Column(String, nullable=False)
    company_id = Column(String, nullable=True)
    # Должность
    position = Column(String, nullable=False)
    position_id = Column(String, nullable=True)
    # Продолжительность работы
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    # Описание
    description = Column(String, nullable=True)
    # Примененные навыки
    skill_set = Column(String, nullable=True)
