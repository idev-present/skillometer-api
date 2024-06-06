from typing import List

from sqlalchemy import Column, String, Integer

from app.core.db.base import BaseDBModel
from sqlalchemy.sql import expression as sql


class CityDBModel(BaseDBModel):
    __tablename__ = 'dict_city'
    id = Column(String(50), primary_key=True)
    fias_id = Column(String(50), nullable=True)
    habr_id = Column(Integer, nullable=True)
    habr_alias = Column(String(50), nullable=True)
    country_name = Column(String(50), nullable=True)
    region_name = Column(String(50), nullable=True)

    @classmethod
    async def get_list(cls, db) -> List["CityDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res


class EmploymentTypeDBModel(BaseDBModel):
    __tablename__ = 'dict_employment_type'
    id = Column(String(50), primary_key=True)
    habr_id = Column(String(50), nullable=True)
    hh_id = Column(String(50), nullable=True)

    @classmethod
    async def get_list(cls, db) -> List["EmploymentTypeDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res


class DivisionDBModel(BaseDBModel):
    __tablename__ = 'dict_division'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=True)
    habr_id = Column(Integer, nullable=True)

    @classmethod
    async def get_list(cls, db) -> List["DivisionDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res


class QualificationDBModel(BaseDBModel):
    __tablename__ = 'dict_qualification'
    id = Column(String(50), primary_key=True)
    name = Column(String(50), nullable=True)
    habr_id = Column(Integer, nullable=True)

    @classmethod
    async def get_list(cls, db) -> List["QualificationDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res
