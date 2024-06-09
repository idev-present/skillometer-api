import datetime
from typing import List

from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.services.vacancy.schemas import VacancyForm, VacancyUpdateForm
from app.utils.database_utils import generate_uid


class VacancyDBModel(BaseDBModel):
    __tablename__ = 'vacancies'

    id = Column(String, primary_key=True)
    # Название
    name = Column(String, nullable=False)
    # * External links
    habr_id = Column(Integer, nullable=True)
    hh_id = Column(Integer, nullable=True)
    url = Column(String, nullable=True)
    # * Config
    salary_from = Column(Integer, nullable=True)
    salary_to = Column(Integer, nullable=True)
    currency = Column(String, nullable=False)
    is_remote = Column(Boolean, nullable=False, default=False)
    # * Description parts
    # Описание вакансии (текст или HTML)
    description = Column(String, nullable=False)
    # О компании и команде
    team = Column(String, nullable=False)
    # Ожидания от кандидата (текст или HTML)
    todo = Column(String, nullable=False)
    # * Dict
    # Город проживания
    city_id = Column(String, nullable=True)
    # Тип занятости
    employment_type_id = Column(String, nullable=True)
    # специализация
    division_id = Column(String, nullable=True)
    # Квалификация
    qualification_id = Column(String, nullable=True)
    # Навыки (от 1 до 10)
    skill_set = Column(String, nullable=True)
    # * Timestamps
    created_at = Column(DateTime, default=datetime.datetime.now)
    published_at = Column(DateTime, default=datetime.datetime.now)
    # * Relationships
    owner_id = Column(String, nullable=True)
    company_id = Column(String, nullable=True)

    @classmethod
    async def create(cls, db, form: VacancyForm) -> "VacancyDBModel":
        vacancy = cls(**form.dict())
        vacancy.id = generate_uid('v')
        db.add(vacancy)
        await db.commit()
        await db.refresh(vacancy)
        return vacancy

    @classmethod
    async def get(cls, db, item_id: str) -> "VacancyDBModel":
        query = sql.select(cls).filter(cls.id == item_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def update(cls, db, item_id: str, form: VacancyUpdateForm) -> "VacancyDBModel":
        vacancy = await cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(vacancy, field, value)
        db.add(vacancy)
        await db.commit()
        await db.refresh(vacancy)
        return vacancy

    @classmethod
    async def delete(cls, db, item_id: str) -> bool:
        vacancy = await cls.get(db, item_id)
        await db.delete(vacancy)
        await db.commit()
        return True

    @classmethod
    async def get_list(cls, db) -> List["VacancyDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res
