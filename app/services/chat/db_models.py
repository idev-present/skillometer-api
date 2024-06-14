from sqlalchemy import Column, UUID, String, Text, DateTime, func, Boolean, Integer

from app.core.db import BaseDBModel


class Message(BaseDBModel):
    id = Column(UUID(as_uuid=True), primary_key=True)
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
    room_id = Column(UUID(as_uuid=True), nullable=True)  # reply_id
    is_deleted = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(UUID(as_uuid=True), nullable=True)


class ChatRoom(BaseDBModel):
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # reply or p2p
    reply_id = Column(UUID(as_uuid=True), nullable=True)
    applicant_id = Column(UUID(as_uuid=True), nullable=True)
    recruiter_id = Column(UUID(as_uuid=True), nullable=True)
    unread_count = Column(Integer, nullable=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean(), default=False)