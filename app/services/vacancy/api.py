from typing import List

from fastapi import APIRouter, Depends, Response

from app.core.db import db_service
from app.services.vacancy.db_models import VacancyDBModel
from app.services.vacancy.schemas import VacancyListItem, Vacancy, VacancyForm

router = APIRouter()


@router.post("/", response_model=Vacancy)
async def create_vacancy(vacancy: VacancyForm, db_session=Depends(db_service.get_db)) -> Vacancy:
    res = await VacancyDBModel.create(db=db_session, form=vacancy)
    return res


@router.get("/{vacancy_id}", response_model=Vacancy)
async def get_vacancy(vacancy_id: str, db_session=Depends(db_service.get_db)) -> Vacancy:
    res = await VacancyDBModel.get(db=db_session, item_id=vacancy_id)
    return res


@router.put("/{vacancy_id}", response_model=Vacancy)
async def update_vacancy(vacancy_id: str, vacancy: VacancyForm, db_session=Depends(db_service.get_db)) -> Vacancy:
    res = await VacancyDBModel.update(db=db_session, item_id=vacancy_id, form=vacancy)
    return res


@router.delete("/{vacancy_id}", response_model=Vacancy)
async def delete_vacancy(vacancy_id: str, db_session=Depends(db_service.get_db)):
    await VacancyDBModel.delete(db=db_session, item_id=vacancy_id)
    return Response(status_code=204, content={"message": "Item has been deleted."})


@router.get("/")
async def vacancy_list(db_session=Depends(db_service.get_db)) -> List[VacancyListItem]:
    res = await VacancyDBModel.get_list(db=db_session)
    return res
