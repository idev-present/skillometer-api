from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from structlog import get_logger

from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.core.exceptions import NotFoundError
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
        lazy='joined',
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
    def get(cls, db, item_id: str) -> "ApplicantDBModel":
        try:
            query = sql.select(cls).where(cls.id == item_id)
            logger.debug(query)
            result = db.execute(query)
            if not result:
                raise HTTPException(status_code=404, detail="Item not found")
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def update(cls, db, item_id: str, form: ApplicantForm) -> "ApplicantDBModel":
        try:
            applicant = cls.get(db, item_id)
            for field, value in form.dict(exclude_unset=True).items():
                setattr(applicant, field, value)
            db.add(applicant)
            db.commit()
            db.refresh(applicant)
            return applicant
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    def delete(cls, db, item_id: str) -> bool:
        applicant = cls.get(db, item_id)
        db.delete(applicant)
        db.commit()
        return True

    @classmethod
    def get_list(cls, db) -> List["ApplicantDBModel"]:
        query = sql.select(cls)
        res = db.execute(query)
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
    def create(cls, form: ApplicantXPForm, parent_id: str, db) -> "ApplicantXPDBModel":
        xp_item = cls(**form.dict())
        xp_item.id = generate_uid('xp')
        xp_item.applicant_id = parent_id
        if xp_item.start_date:
            xp_item.start_date = datetime.fromtimestamp(xp_item.start_date.timestamp())
        if xp_item.end_date:
            xp_item.end_date = datetime.fromtimestamp(xp_item.end_date.timestamp())
        db.add(xp_item)
        db.commit()
        db.refresh(xp_item)
        return xp_item

    @classmethod
    def get(cls, db, item_id: str) -> "ApplicantXPDBModel":
        query = sql.select(cls).where(cls.id == item_id)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def update(cls, db, item_id: str, form: ApplicantXPUpdateForm) -> "ApplicantXPDBModel":
        xp_item = cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(xp_item, field, value)

        if xp_item.start_date:
            xp_item.start_date = datetime.fromtimestamp(xp_item.start_date.timestamp())
        if xp_item.end_date:
            xp_item.end_date = datetime.fromtimestamp(xp_item.end_date.timestamp())
        db.add(xp_item)
        db.commit()
        db.refresh(xp_item)
        return xp_item

    @classmethod
    def delete(cls, db, item_id: str) -> bool:
        applicant = cls.get(db, item_id)
        db.delete(applicant)
        db.commit()
        return True

    @classmethod
    def get_list(cls, parent_id: str, db) -> List["ApplicantXPDBModel"]:
        query = sql.select(cls).where(cls.applicant_id == parent_id)
        res = db.execute(query)
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
    def create(cls, form: ApplicantEducationForm, parent_id: str, db) -> "ApplicantEducationDBModel":
        edu_item = cls(**form.dict())
        edu_item.id = generate_uid('edu')
        edu_item.applicant_id = parent_id
        if edu_item.start_date:
            edu_item.start_date = datetime.fromtimestamp(edu_item.start_date.timestamp())
        if edu_item.end_date:
            edu_item.end_date = datetime.fromtimestamp(edu_item.end_date.timestamp())
        db.add(edu_item)
        db.commit()
        db.refresh(edu_item)
        return edu_item

    @classmethod
    def get(cls, db, item_id: str) -> "ApplicantEducationDBModel":
        query = sql.select(cls).where(cls.id == item_id)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def update(cls, db, item_id: str, form: ApplicantEducationUpdateForm) -> "ApplicantEducationDBModel":
        edu_item = cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(edu_item, field, value)

        if edu_item.start_date:
            edu_item.start_date = datetime.fromtimestamp(edu_item.start_date.timestamp())
        if edu_item.end_date:
            edu_item.end_date = datetime.fromtimestamp(edu_item.end_date.timestamp())
        db.add(edu_item)
        db.commit()
        db.refresh(edu_item)
        return edu_item

    @classmethod
    def delete(cls, db, item_id: str) -> bool:
        edu_item = cls.get(db, item_id)
        db.delete(edu_item)
        db.commit()
        return True

    @classmethod
    def get_list(cls, parent_id: str, db) -> List["ApplicantEducationDBModel"]:
        query = sql.select(cls).where(cls.applicant_id == parent_id)
        res = db.execute(query)
        res = res.scalars().all()

        return res
