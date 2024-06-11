from typing import List

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.services.applicant.schemas import ApplicantForm


class ApplicantDBModel(BaseDBModel):
    __tablename__ = 'applicants'

    id = Column(String, primary_key=True)
    salary_from = Column(Integer, nullable=True)
    currency = Column(String(50), nullable=True)
    is_relocation = Column(Boolean, default=False)
    is_remote = Column(Boolean, default=False)
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
    # * Computed fields
    experience = Column(String)
    age = Column(Integer, nullable=True)
    title = Column(String, nullable=False)

    # * Timestamps
    registered_at = Column(DateTime, nullable=True)
    last_visited = Column(DateTime, nullable=True)
    # * Relationships
    user_id = mapped_column(ForeignKey('users.id'))
    user = relationship(
        "UserDBModel",
        back_populates="applicant"
    )

    @classmethod
    async def get(cls, db, item_id: str) -> "ApplicantDBModel":
        query = sql.select(ApplicantDBModel).where(cls.id == item_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def update(cls, db, item_id: str, form: ApplicantForm) -> "ApplicantDBModel":
        applicant = await cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(applicant, field, value)
        db.add(applicant)
        await db.commit()
        await db.refresh(applicant)
        return applicant

    @classmethod
    async def delete(cls, db, item_id: str) -> bool:
        applicant = await cls.get(db, item_id)
        await db.delete(applicant)
        await db.commit()
        return True

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
