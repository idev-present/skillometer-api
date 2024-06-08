from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.applicant.db_models import ApplicantDBModel
from app.services.applicant.schemas import Applicant

router = APIRouter()


@router.get("/")
async def applicant_list(db_session=Depends(db_service.get_db)) -> List[Applicant]:
    res = await ApplicantDBModel.get_list(db_session)
    return res