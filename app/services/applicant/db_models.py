from datetime import datetime
from typing import List
from structlog import get_logger

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.services.applicant.schemas import ApplicantForm, ApplicantXPForm, ApplicantXPUpdateForm, \
    ApplicantEducationForm, ApplicantEducationUpdateForm
from app.utils.database_utils import generate_uid, get_result_query

logger = get_logger(__name__)


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
    xp = relationship(
        "ApplicantXPDBModel",
        order_by="desc(ApplicantXPDBModel.start_date)",
        back_populates='applicant'
    )
    education = relationship(
        "ApplicantEducationDBModel",
        order_by="desc(ApplicantEducationDBModel.start_date)",
        back_populates='applicant'
    )

    @classmethod
    async def get(cls, db, item_id: str) -> "ApplicantDBModel":
        query = sql.select(cls).where(cls.id == item_id)
        logger.debug(query)
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

    id = mapped_column(String, primary_key=True)
    applicant_id = Column(String(50), ForeignKey('applicants.id'), nullable=False)
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
    # * Relationships
    applicant = relationship(
        "ApplicantDBModel",
        back_populates='xp'
    )

    @classmethod
    async def create(cls, form: ApplicantXPForm, parent_id: str, db) -> "ApplicantXPDBModel":
        xp_item = cls(**form.dict())
        xp_item.id = generate_uid('xp')
        xp_item.applicant_id = parent_id
        if xp_item.start_date:
            xp_item.start_date = datetime.fromtimestamp(xp_item.start_date.timestamp())
        if xp_item.end_date:
            xp_item.end_date = datetime.fromtimestamp(xp_item.end_date.timestamp())
        db.add(xp_item)
        await db.commit()
        await db.refresh(xp_item)
        return xp_item

    @classmethod
    async def get(cls, db, item_id: str) -> "ApplicantXPDBModel":
        query = sql.select(cls).where(cls.id == item_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def update(cls, db, item_id: str, form: ApplicantXPUpdateForm) -> "ApplicantXPDBModel":
        xp_item = await cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(xp_item, field, value)

        if xp_item.start_date:
            xp_item.start_date = datetime.fromtimestamp(xp_item.start_date.timestamp())
        if xp_item.end_date:
            xp_item.end_date = datetime.fromtimestamp(xp_item.end_date.timestamp())
        db.add(xp_item)
        await db.commit()
        await db.refresh(xp_item)
        return xp_item

    @classmethod
    async def delete(cls, db, item_id: str) -> bool:
        applicant = await cls.get(db, item_id)
        await db.delete(applicant)
        await db.commit()
        return True

    @classmethod
    async def get_list(cls, parent_id: str, db) -> List["ApplicantXPDBModel"]:
        query = sql.select(cls).where(cls.applicant_id == parent_id)
        res = await db.execute(query)
        res = res.scalars().all()

        return res


class ApplicantEducationDBModel(BaseDBModel):
    __tablename__ = 'applicant_education'

    id = mapped_column(String, primary_key=True)
    applicant_id = Column(String(50), ForeignKey('applicants.id'), nullable=False)
    # Название заведения
    university_name = Column(String, nullable=False)
    university_id = Column(String, nullable=True)
    # Факультет
    faculty_name = Column(String, nullable=False)
    faculty_id = Column(String, nullable=True)
    # Местоположение учебного заведения
    city_id = Column(String(50), nullable=True)
    # Продолжительность учёбы
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    # Специализация
    specialization = Column(String, nullable=True)
    # * Relationships
    applicant = relationship(
        "ApplicantDBModel",
        back_populates='education'
    )

    @classmethod
    async def create(cls, form: ApplicantEducationForm, parent_id: str, db) -> "ApplicantEducationDBModel":
        edu_item = cls(**form.dict())
        edu_item.id = generate_uid('edu')
        edu_item.applicant_id = parent_id
        if edu_item.start_date:
            edu_item.start_date = datetime.fromtimestamp(edu_item.start_date.timestamp())
        if edu_item.end_date:
            edu_item.end_date = datetime.fromtimestamp(edu_item.end_date.timestamp())
        db.add(edu_item)
        await db.commit()
        await db.refresh(edu_item)
        return edu_item

    @classmethod
    async def get(cls, db, item_id: str) -> "ApplicantEducationDBModel":
        query = sql.select(cls).where(cls.id == item_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def update(cls, db, item_id: str, form: ApplicantEducationUpdateForm) -> "ApplicantEducationDBModel":
        edu_item = await cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(edu_item, field, value)

        if edu_item.start_date:
            edu_item.start_date = datetime.fromtimestamp(edu_item.start_date.timestamp())
        if edu_item.end_date:
            edu_item.end_date = datetime.fromtimestamp(edu_item.end_date.timestamp())
        db.add(edu_item)
        await db.commit()
        await db.refresh(edu_item)
        return edu_item

    @classmethod
    async def delete(cls, db, item_id: str) -> bool:
        edu_item = await cls.get(db, item_id)
        await db.delete(edu_item)
        await db.commit()
        return True

    @classmethod
    async def get_list(cls, parent_id: str, db) -> List["ApplicantEducationDBModel"]:
        query = sql.select(cls).where(cls.applicant_id == parent_id)
        res = await db.execute(query)
        res = res.scalars().all()

        return res
