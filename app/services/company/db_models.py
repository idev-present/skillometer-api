from sqlalchemy import Column, String, Boolean

from app.core.db import BaseDBModel


class CompanyDBModel(BaseDBModel):
    __tablename__ = 'companies'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    subtitle = Column(String, nullable=True)
    href = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    accredited = Column(Boolean)

    habr_id = Column(String, nullable=True)
