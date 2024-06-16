import uuid
from typing import List

from sqlalchemy import Column, UUID, String, Text, DateTime, func, Boolean, Integer, ForeignKey, sql
from sqlalchemy.orm import mapped_column, relationship

from app.core.db import BaseDBModel
from app.services.chat.schemas import ChatRoomForm, ChatRoomUpdateForm, MessageForm, MessageUpdateForm


class ChatRoomDBModel(BaseDBModel):
    __tablename__ = 'chat_rooms'
    # * Config
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # reply or p2p
    reply_id = Column(UUID(as_uuid=True), nullable=True)
    applicant_id = Column(UUID(as_uuid=True), nullable=True)
    recruiter_id = Column(UUID(as_uuid=True), nullable=True)
    unread_count = Column(Integer, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean(), default=False)
    # * Relationships
    messages = relationship(
        "MessageDBModel",
        order_by="desc(MessageDBModel.created_at)",
        back_populates='room'
    )

    @classmethod
    def create(cls, db, form: ChatRoomForm) -> "ChatRoomDBModel":
        room = cls(**form.dict())
        room.id = uuid.uuid4()
        room.type = form.type.value
        db.add(room)
        db.commit()
        db.refresh(room)
        return room

    @classmethod
    def get(cls, db, item_id: str) -> "ChatRoomDBModel":
        query = sql.select(cls).filter(cls.id == item_id)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def update(cls, db, item_id: str, form: ChatRoomUpdateForm) -> "ChatRoomDBModel":
        room = cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(room, field, value)
        db.add(room)
        db.commit()
        db.refresh(room)
        return room

    @classmethod
    def delete(cls, db, item_id: str) -> bool:
        room = cls.get(db, item_id)
        db.delete(room)
        db.commit()
        return True


class MessageDBModel(BaseDBModel):
    __tablename__ = "chat_messages"
    # Config
    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    type = Column(String(50), nullable=False)  # text | link | file | image
    status = Column(String(50), nullable=False)  # sent | read |
    has_entities = Column(String, nullable=True)  # Set of types of the entity. Currently, can be “mention” (@username),
    # “hashtag” (#hashtag), “cashtag” ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org),
    # “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text), “italic” (italic
    # text), “underline” (underlined text), “strikethrough” (strikethrough text), “spoiler” (spoiler message),
    # “blockquote” (block quotation), “expandable_blockquote” (collapsed-by-default block quotation),
    # “code” (monowidth string), “pre” (monowidth block), “text_link” (for clickable text URLs), “text_mention” (for
    # users without usernames), “custom_emoji” (for inline custom emoji stickers)
    content = Column(Text)
    from_id = Column(UUID(as_uuid=True), nullable=True)
    to_id = Column(UUID(as_uuid=True), nullable=True)
    room_id = Column(UUID(as_uuid=True), ForeignKey('chat_rooms.id'), nullable=True)  # room if not p2p
    is_deleted = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    # * Relationships
    room = relationship(
        "ChatRoomDBModel",
        back_populates='messages'
    )

    @classmethod
    def create(cls, db, form: MessageForm) -> "MessageDBModel":
        message = cls(**form.dict())
        message.id = uuid.uuid4()
        message.type = form.type.value
        message.status = form.status.value
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @classmethod
    def get(cls, db, item_id: str) -> "MessageDBModel":
        query = sql.select(cls).filter(cls.id == item_id)
        result = db.execute(query)
        return result.scalars().first()

    @classmethod
    def update(cls, db, item_id: str, form: MessageUpdateForm) -> "MessageDBModel":
        message = cls.get(db, item_id)
        for field, value in form.dict(exclude_unset=True).items():
            setattr(message, field, value)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    @classmethod
    def delete(cls, db, item_id: str) -> bool:
        message = cls.get(db, item_id)
        db.delete(message)
        db.commit()
        return True

    @classmethod
    def get_list(cls, room_id: str, db) -> List["MessageDBModel"]:
        query = sql.select(cls).where(cls.room_id == room_id)
        res = db.execute(query)
        res = res.scalars().all()

        return res