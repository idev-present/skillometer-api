from operator import itemgetter
from typing import List, Optional
from uuid import UUID

import arrow
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette import status

from app.core.db import db_service
from app.services.applicant.db_models import ApplicantDBModel
from app.services.event.db_models import EventDBModel
from app.services.event.schemas import Event, EventForm, EventInput, EVENT_STATUS, EventUpdateForm, EventFilters
from app.services.reply.db_models import ReplyDBModel

router = APIRouter()


@router.post("/", response_model=Event)
def create_event(reply_id: str, form: EventForm, db_session=Depends(db_service.get_db)):
    reply = ReplyDBModel.get(item_id=reply_id, db=db_session)
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reply #{reply_id} not found")
    applicant = ApplicantDBModel.get(item_id=reply.applicant_id, db=db_session)
    if not applicant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Applicant #{reply.applicant_id} not found")
    if not reply.owner_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Reply dont have owner id")
    input_data = EventInput(
        status=EVENT_STATUS.PLANNING,
        owner_id=reply.owner_id,
        to_id=applicant.user_id,
        reply_id=reply_id,
        name=form.name,
        type=form.type,
        payload=form.payload,
        description=form.description,
        start_at=form.start_at,
        end_at=form.end_at,
    )
    event = EventDBModel.create(form=input_data, db=db_session)
    return event


@router.get("/", response_model=List[Event])
def get_event_list(db_session=Depends(db_service.get_db), applicant_id: Optional[UUID] = None,
                   recruiter_id: Optional[UUID] = None, status: Optional[EVENT_STATUS] = None):
    filters = EventFilters(
        applicant_id=applicant_id,
        recruiter_id=recruiter_id,
        status=status
    )
    events = EventDBModel.get_list(filters=filters, db=db_session)
    return events


@router.get("/available/days", response_model=List[str])
def get_available_days():
    # Получить текущую дату
    start_date = arrow.now()

    # Создать список для хранения рабочих дней
    working_days = []

    # Добавить дни без выходных в следующие две недели
    for i in range(14):
        date = start_date.shift(days=i)

        # проверка на выходные
        if date.weekday() < 5:  # 0-4 - рабочие дни, 5-6 - выходные
            working_days.append(date.format('YYYY-MM-DD'))

    return working_days


@router.get("/available/time")
def get_available_time(reply_id: str, day: str, db_session=Depends(db_service.get_db)):
    reply = ReplyDBModel.get(item_id=reply_id, db=db_session)
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Reply #{reply_id} not found")

    start_date = arrow.get(day, 'YYYY-MM-DD').to("Europe/Moscow").replace(hour=8, minute=0, second=0, microsecond=0)
    end_date = arrow.get(day, 'YYYY-MM-DD').to("Europe/Moscow").replace(hour=19, minute=59, second=0, microsecond=0)

    filters = EventFilters(
        start_date=start_date.datetime,
        end_date=end_date.datetime,
        recruiter_id=reply.owner_id
    )

    current_events = EventDBModel.get_list(filters=filters, db=db_session)

    def formate_reserved_times(current_events):
        return [(event.start_at, event.end_at) for event in current_events]

    reserved_times = formate_reserved_times(current_events)

    days_slots = []
    for hour_range in arrow.Arrow.span_range('hour', start_date, end_date):
        days_slots.append([hour_range[0].format(), hour_range[1].format()])

    available_slots_without_overlap = []
    for slot in days_slots:
        # Использование Arrow для создания объектов даты и времени.
        slot_start = arrow.get(itemgetter(0)(slot))
        slot_end = arrow.get(itemgetter(1)(slot))

        # Проверка пересечений со всеми зарезервированными интервалами.
        if not any(arrow.get(itemgetter(0)(interval)) < slot_end and arrow.get(itemgetter(1)(interval)) > slot_start for
                   interval in reserved_times):
            # Если пересечения нет, добавить слот в результирующий список.
            available_slots_without_overlap.append(slot)

    return available_slots_without_overlap


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: UUID, db_session=Depends(db_service.get_db)):
    event = EventDBModel.get(item_id=event_id, db=db_session)
    return event


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: UUID, form: EventUpdateForm, db_session=Depends(db_service.get_db)):
    event = EventDBModel.update(item_id=event_id, form=form, db=db_session)
    return event


@router.delete("/{event_id}")
def delete_event(event_id: UUID, db_session=Depends(db_service.get_db)):
    EventDBModel.delete(item_id=event_id, db=db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
