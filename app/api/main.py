from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.services.dict.api import router as dict_router
from app.services.vacancy.api import router as vacancy_router
from app.services.company.api import router as company_router
from app.services.applicant.api import router as applicant_router
from app.services.reply.api import router as reply_router

api = APIRouter()
api.include_router(dict_router, prefix="/dict", tags=["dict"])
api.include_router(vacancy_router, prefix="/vacancy", tags=["vacancy"])
api.include_router(company_router, prefix="/company", tags=["company"])
api.include_router(applicant_router, prefix="/applicant", tags=["applicant"])
api.include_router(reply_router, prefix="/reply", tags=["reply"])
