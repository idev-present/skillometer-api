from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.core.db import db_service
from app.services.applicant.schemas import Applicant

router = APIRouter()


@router.post("/")
async def login(request: Request, db_session=Depends(db_service.get_db)) -> List[Applicant]:
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    sdk = request.app.state.CASDOOR_SDK
    return res