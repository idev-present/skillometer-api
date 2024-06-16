from sqlalchemy import Column, String, ForeignKey, UUID, Boolean, DateTime, func
from sqlalchemy.orm import mapped_column

from app.core.db import BaseDBModel


class EventDBModel(BaseDBModel):
    __tablename__ = 'events'

    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(50), nullable=False)  # ZOOM | GOOGLE_MEET | TELEGRAM | PHONE
    status = Column(String(50), nullable=False)  # PLANNING | CONFIRMED | WAITING |DONE
    payload = Column(String, nullable=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # id рекрутера
    to_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)  # id соискателя
    reply_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    is_deleted = Column(Boolean(), default=False)
    start_at = Column(DateTime(timezone=True), nullable=True)  # Дата+время начала
    end_at = Column(DateTime(timezone=True), nullable=True)  # Дата+время завершения
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), nullable=True)
