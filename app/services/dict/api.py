from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy_utils import Currency

from app.core.db import db_service
from app.services.dict.const import CURRENCY, REPLY_STATUS
from app.services.dict.db_models import (
    CityDBModel,
    EmploymentTypeDBModel,
    DivisionDBModel,
    QualificationDBModel,
    SearchStatusDBModel,
    SkillDBModel
)
from app.services.dict.schemas import (
    City,
    EmploymentType,
    Division,
    Qualification,
    SearchStatus,
    Skill, KeyValueDict
)

router = APIRouter()


# TODO(i.zhuravlev): move to utils
def get_enum_members(enum_class):
    return enum_class.__members__.items()


@router.get("/currency", response_model=List[KeyValueDict])
def get_currency_list():
    return [
        {"key": name, "value": currency.value}
        for name, currency in get_enum_members(CURRENCY)
    ]


@router.get("/city", response_model=List[City])
async def city_list(db_session=Depends(db_service.get_db)) -> List[City]:
    res = CityDBModel.get_list(db_session)
    return res


@router.get("/employment_type", response_model=List[EmploymentType])
async def employment_type_list(db_session=Depends(db_service.get_db)):
    res = EmploymentTypeDBModel.get_list(db_session)
    return res


@router.get("/division", response_model=List[Division])
async def division_list(db_session=Depends(db_service.get_db)):
    res = DivisionDBModel.get_list(db_session)
    return res


@router.get("/qualification", response_model=List[Qualification])
async def qualification_list(db_session=Depends(db_service.get_db)):
    res = QualificationDBModel.get_list(db_session)
    return res


@router.get("/search_status", response_model=List[SearchStatus])
async def search_status_list(db_session=Depends(db_service.get_db)):
    res = SearchStatusDBModel.get_list(db_session)
    return res


@router.get("/skill", response_model=List[Skill])
async def skill_list(db_session=Depends(db_service.get_db)):
    res = SkillDBModel.get_list(db_session)
    return res


@router.get("/reply_status", response_model=List[KeyValueDict])
def reply_status_list():
    return [
        {"key": name, "value": currency.value}
        for name, currency in get_enum_members(REPLY_STATUS)
    ]