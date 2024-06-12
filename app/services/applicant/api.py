from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response
from starlette import status

from app.core.db import db_service
from app.services.applicant.db_models import ApplicantDBModel
from app.services.applicant.schemas import Applicant, ApplicantListItem, ApplicantForm, ApplicantUpdateForm

router = APIRouter()


@router.get("/{applicant_id}", response_model=Applicant)
async def get_applicant(applicant_id: str, db: Session = Depends(db_service.get_db)) -> Applicant:
    res = await ApplicantDBModel.get(db=db, item_id=applicant_id)
    return res


@router.put("/{applicant_id}", response_model=Applicant)
async def update_applicant(applicant_id: str, form: ApplicantUpdateForm, db: Session = Depends(db_service.get_db)) -> Applicant:
    res = await ApplicantDBModel.update(db=db, item_id=applicant_id, form=form)
    return res


@router.delete("/{applicant_id}")
async def delete_applicant(applicant_id: str, db: Session = Depends(db_service.get_db)):
    await ApplicantDBModel.delete(db=db, item_id=applicant_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/", response_model=List[ApplicantListItem])
async def applicant_list(db_session=Depends(db_service.get_db)) -> List[ApplicantListItem]:
    res = await ApplicantDBModel.get_list(db_session)
    return res