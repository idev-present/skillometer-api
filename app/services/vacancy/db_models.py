import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime

from app.core.db import BaseDBModel


class VacancyDBModel(BaseDBModel):
    __tablename__ = 'vacancies'

    id = Column(String, primary_key=True)
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
    city_id = Column(Integer, nullable=True)
    # Тип занятости
    employment_type_id = Column(String, nullable=True)
    # специализация
    division_id = Column(String, nullable=True)
    # Квалификация
    qualification_id = Column(String, nullable=True)
    # Навыки (от 1 до 10)
    skills = Column(String, nullable=True)
    # * Timestamps
    created_at = Column(DateTime, default=datetime.datetime.now)
    published_at = Column(DateTime, default=datetime.datetime.now)
    # * Relationships
    owner_id = Column(String, nullable=True)
    company_id = Column(String, nullable=True)