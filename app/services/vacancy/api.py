import json
from typing import List

from fastapi import APIRouter, Depends, Response, HTTPException
from starlette import status

from app.core.db import db_service
from app.core.iam.schemas import TokenData
from app.services.processing.main import create_reply
from app.services.user.middlewares import get_current_user
from app.services.vacancy.db_models import VacancyDBModel
from app.services.vacancy.schemas import VacancyListItem, Vacancy, VacancyForm, VacancyUpdateForm

router = APIRouter()


@router.post("/", response_model=Vacancy)
def create_vacancy(form: VacancyForm, db_session=Depends(db_service.get_db)) -> Vacancy:
    res = VacancyDBModel.create(db=db_session, form=form)
    return res


@router.get("/{vacancy_id}", response_model=Vacancy)
def get_vacancy(vacancy_id: str, db_session=Depends(db_service.get_db)) -> Vacancy:
    res = VacancyDBModel.get(db=db_session, item_id=vacancy_id)
    return res


@router.put("/{vacancy_id}", response_model=Vacancy)
def update_vacancy(vacancy_id: str, vacancy: VacancyUpdateForm, db_session=Depends(db_service.get_db)) -> Vacancy:
    res = VacancyDBModel.update(db=db_session, item_id=vacancy_id, form=vacancy)
    return res


@router.delete("/{vacancy_id}")
def delete_vacancy(vacancy_id: str, db_session=Depends(db_service.get_db)):
    VacancyDBModel.delete(db=db_session, item_id=vacancy_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{vacancy_id}/reply")
def vacancy_reply(vacancy_id: str, token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    res = create_reply(user_id=token_data.id, vacancy_id=vacancy_id, applicant_id=token_data.name, db=db_session)
    return res


@router.get("/", response_model=List[VacancyListItem])
def vacancy_list(db_session=Depends(db_service.get_db)) -> List[VacancyListItem]:
    res = VacancyDBModel.get_list(db=db_session)
    return res
