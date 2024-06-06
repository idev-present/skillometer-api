from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.vacancy.db_models import VacancyDBModel
from app.services.vacancy.schemas import Vacancy

router = APIRouter()


@router.get("/")
async def vacancy_list(db_session=Depends(db_service.get_db)) -> List[Vacancy]:
    res = await VacancyDBModel.get_list(db_session)
    return res
