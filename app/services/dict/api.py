from typing import List

from fastapi import APIRouter, Depends

from app.core.db import db_service
from app.services.dict.const import CURRENCY
from app.services.dict.db_models import CityDBModel, EmploymentTypeDBModel, DivisionDBModel, QualificationDBModel
from app.services.dict.schemas import City, EmploymentType, Division, Qualification, Currency

router = APIRouter()


# TODO(i.zhuravlev): move to utils
def get_enum_members(enum_class):
    return enum_class.__members__.items()


@router.get("/currency")
def get_currency_list() -> List[Currency]:
    return [
        {"key": name, "value": currency.value}
        for name, currency in get_enum_members(CURRENCY)
    ]


@router.get("/city")
async def city_list(db_session=Depends(db_service.get_db)) -> List[City]:
    res = await CityDBModel.get_list(db_session)
    return res


@router.get("/employment_type")
async def employment_type_list(db_session=Depends(db_service.get_db)) -> List[EmploymentType]:
    res = await EmploymentTypeDBModel.get_list(db_session)
    return res


@router.get("/division")
async def division_list(db_session=Depends(db_service.get_db)) -> List[Division]:
    res = await DivisionDBModel.get_list(db_session)
    return res


@router.get("/qualification")
async def qualification_list(db_session=Depends(db_service.get_db)) -> List[Qualification]:
    res = await QualificationDBModel.get_list(db_session)
    return res
