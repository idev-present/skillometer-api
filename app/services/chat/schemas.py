from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from app.services.chat.const import MESSAGE_TYPE, MESSAGE_STATUS, CHAT_ROOM_TYPE


class MessageForm(BaseModel):
    type: MESSAGE_TYPE = Field(..., description="Тип сообщения")
    content: str = Field(..., description="Текст сообщения")
    status: Optional[MESSAGE_STATUS] = Field(None, description="Статус сообщения")
    from_id: Optional[UUID] = Field(None, description="UUID отправителя. Может быть пустым")
    to_id: Optional[UUID] = Field(None, description="UUID получателя. Может быть пустым")
    room_id: Optional[UUID] = Field(None, description="UUID комнаты. Может быть пустым")


class MessageUpdateForm(MessageForm):
    type: Optional[MESSAGE_TYPE] = Field(None, description="Тип сообщения")
    content: Optional[str] = Field(None, description="Текст сообщения")


class SendMessage(BaseModel):
    type: Optional[MESSAGE_TYPE] = Field(None, description="Тип сообщения")
    content: Optional[str] = Field(None, description="Текст сообщения")


class Message(MessageForm):
    id: UUID = Field(..., description="UUID сообщения")
    created_at: datetime = Field(..., description="Время создания сообщения")
    updated_at: Optional[datetime] = Field(None, description="Время последнего обновления сообщения")
    updated_by: Optional[str] = Field(None, description="UUID пользователя, который последний раз обновил сообщение")
    is_deleted: Optional[bool] = Field(False, description="Флаг удаления сообщения")
    has_entities: Optional[str] = Field(None, description="Используемые сущности в сообщении")


class ChatRoomForm(BaseModel):
    name: str = Field(..., title="Имя", description="Имя чата")
    type: CHAT_ROOM_TYPE = Field(..., title="Тип", description="Тип чата: reply или p2p")
    reply_id: Optional[UUID] = Field(None, title="ID ответа", description="ID отклика, если тип чата - reply")
    applicant_id: Optional[UUID] = Field(None, title="ID соискателя", description="ID соискателя")
    recruiter_id: Optional[UUID] = Field(None, title="ID рекрутера", description="ID рекрутера")
    unread_count: Optional[int] = Field(None, title="Счетчик непрочитанных сообщений",
                                        description="Количество непрочитанных сообщений в чате")
    is_deleted: Optional[bool] = Field(False, title="Удален", description="Признак, был ли удален чат")


class ChatRoomUpdateForm(ChatRoomForm):
    name: Optional[str] = Field(None, title="Имя", description="Имя чата")
    type: Optional[CHAT_ROOM_TYPE] = Field(None, title="Тип", description="Тип чата: reply или p2p")


class ChatRoom(ChatRoomForm):
    id: UUID = Field(..., title="ID", description="Уникальный идентификатор чата")
    type: str = Field(..., title="Тип", description="Тип чата: reply или p2p")
    last_updated: datetime = Field(..., title="Последнее обновление", description="Время последнего обновления чата")
