from datetime import datetime
from typing import List

from sqlalchemy import Column, String, DateTime, UUID
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import expression as sql

from app.core.db import BaseDBModel
from app.services.user.schemas import User, UserUpdateForm
from app.services.applicant.db_models import ApplicantDBModel # noqa


class UserDBModel(BaseDBModel):
    __tablename__ = 'users'

    id = mapped_column(UUID, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    # * Config
    avatar = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    full_name = Column(String, nullable=False)
    birthday = Column(DateTime, nullable=True)
    bio = Column(String, nullable=True)
    role = Column(String, nullable=False)
    city = Column(String, nullable=True)
    # * Primary contacts
    country_code = Column(String, nullable=True, default="RU")
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    # * Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    # * Relationships
    applicant = relationship(
        "ApplicantDBModel",
        back_populates="user",
        uselist=False
    )

    @classmethod
    async def create(cls, db, form: User) -> "UserDBModel":
        user = cls(**form.dict())
        if user.birthday:
            user.birthday = datetime.fromtimestamp(user.birthday.timestamp())
        if user.created_at:
            user.created_at = datetime.fromtimestamp(user.created_at.timestamp())
        if user.updated_at:
            user.updated_at = datetime.fromtimestamp(user.updated_at.timestamp())
        if user.deleted_at:
            user.deleted_at = datetime.fromtimestamp(user.deleted_at.timestamp())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def get(cls, db, item_id: str) -> "UserDBModel":
        query = sql.select(cls).filter(cls.id == item_id)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def update(cls, db, item_id: str, form: UserUpdateForm) -> "UserDBModel":
        user = await cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(user, field, value)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @classmethod
    async def delete(cls, db, item_id: str) -> bool:
        user = await cls.get(db, item_id)
        await db.delete(user)
        await db.commit()
        return True

    @classmethod
    async def get_list(cls, db) -> List["UserDBModel"]:
        query = sql.select(cls)
        res = await db.execute(query)
        res = res.scalars().all()

        return res
