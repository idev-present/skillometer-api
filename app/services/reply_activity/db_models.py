from sqlalchemy import Column, UUID, String, Text, ForeignKey, DateTime, func

from app.core.db import BaseDBModel


class ActivityDBModel(BaseDBModel):
    __tablename__ = 'reply_activity'

    id = Column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(50), nullable=False)  # REPLY_STATUS | EVENT_STATUS
    text = Column(Text, nullable=True)
    external_id = Column(String(50), nullable=True)  # reply_id | event_id
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    owner_type = Column(String(50), nullable=True)  # user.role
    created_at = Column(DateTime(timezone=True), server_default=func.now())
