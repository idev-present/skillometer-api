from typing import List, Optional
from uuid import UUID

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


@router.get("/{event_id}", response_model=Event)
def read_event(event_id: UUID, db_session=Depends(db_service.get_db)):
    event = EventDBModel.get(item_id=event_id, db=db_session)
    return event


@router.put("/{event_id}", response_model=Event)
def update_event(event_id: UUID, form: EventUpdateForm, db_session=Depends(db_service.get_db)):
    # 1d31ac25-5864-4e96-83f0-475eec5e297f
    # {
    #   "start_at": "2024-06-17T12:00:00.229Z",
    #   "end_at": "2024-06-17T12:59:49.229Z"
    # }
    event = EventDBModel.update(item_id=event_id, form=form, db=db_session)
    return event


@router.delete("/{event_id}")
def delete_event(event_id: UUID, db_session=Depends(db_service.get_db)):
    EventDBModel.delete(item_id=event_id, db=db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[Event])
def get_events(db_session=Depends(db_service.get_db), applicant_id: Optional[UUID] = None,
               recruiter_id: Optional[UUID] = None, status: Optional[EVENT_STATUS] = None):
    filters = EventFilters(
        applicant_id=applicant_id,
        recruiter_id=recruiter_id,
        status=status
    )
    events = EventDBModel.get_list(filters=filters, db=db_session)
    return events
