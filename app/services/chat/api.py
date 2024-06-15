from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import update, and_

from app.core.db import db_service
from app.core.exceptions import NotFoundError
from app.services.applicant.db_models import ApplicantDBModel
from app.services.chat.const import CHAT_ROOM_TYPE, MESSAGE_STATUS
from app.services.chat.db_models import ChatRoomDBModel, MessageDBModel
from app.services.chat.schemas import ChatRoomForm, ChatRoom, Message, MessageForm, MessageUpdateForm, \
    ChatRoomUpdateForm
from app.services.reply.db_models import ReplyDBModel

router = APIRouter()


@router.post("/room", response_model=ChatRoom)
def create_room(db_session=Depends(db_service.get_db)):
    # TODO: При создании отклика по дефолту нужно создавать новую комнату на основе данных отклика
    # TODO: Сразу после создания комнаты в базе, нужно создавать папку в бакете
    # FIXME: hardcode
    reply_id = 'a5c6a2d2-d98d-4948-a2d5-d2e664d8556a'
    reply = ReplyDBModel.get(item_id=reply_id, db=db_session)
    applicant = ApplicantDBModel.get(item_id=reply.applicant_id, db=db_session)
    chat_room = ChatRoomForm(
        name=reply.vacancy_name,
        type=CHAT_ROOM_TYPE.REPLY,
        reply_id=reply.id,
        applicant_id=applicant.user_id
    )
    room = ChatRoomDBModel.create(form=chat_room, db=db_session)
    return room


@router.post("/room/{room_id}/message", response_model=Message)
def send_message(room_id: str, form: MessageForm, db_session=Depends(db_service.get_db)):
    chat_room = ChatRoomDBModel.get(item_id=room_id, db=db_session)
    if not chat_room:
        raise NotFoundError(message=f"Room {room_id} not found")
    # FIXME: hardcode
    form.from_id = '43a49b3f-e1ba-4a0e-9229-fb640aee4f00'
    form.to_id = '178fc180-93e9-4446-8fce-8b16ddbb6d50'
    form.room_id = chat_room.id
    form.status = MESSAGE_STATUS.SENT
    message = MessageDBModel.create(form=form, db=db_session)
    update_form = ChatRoomUpdateForm(unread_count=(chat_room.unread_count + 1))
    ChatRoomDBModel.update(item_id=chat_room.id, form=update_form, db=db_session)
    return message


@router.post("/room/{room_id}/message/{message_id}/read_before", response_model=Message)
def read_message(room_id: str, message_id: str, db_session=Depends(db_service.get_db)):
    chat_room = ChatRoomDBModel.get(item_id=room_id, db=db_session)
    if not chat_room:
        raise NotFoundError(message=f"Room {room_id} not found")
    origin_message = MessageDBModel.get(item_id=message_id, db=db_session)
    query = update(MessageDBModel).where(
        and_(MessageDBModel.created_at < origin_message.created_at, MessageDBModel.room_id == room_id)).values(
        status=MESSAGE_STATUS.READ.value)
    res = db_session.execute(query)
    update_form = ChatRoomUpdateForm(unread_count=(chat_room.unread_count - len(res)))
    ChatRoomDBModel.update(item_id=chat_room.id, form=update_form, db=db_session)
    return True


@router.get("/room/{room_id}/history", response_model=List[Message])
def read_history(room_id: str, db_session=Depends(db_service.get_db)):
    message_list = MessageDBModel.get_list(room_id=room_id, db=db_session)
    return message_list