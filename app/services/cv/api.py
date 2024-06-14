from fastapi import APIRouter, Depends
from structlog import get_logger

from app.core.db import db_service
from app.core.iam.schemas import TokenData
from app.services.cv.main import load_user_cv
from app.services.cv.schemas import CV
from app.services.user.middlewares import get_current_user

router = APIRouter()

logger = get_logger(__name__)


@router.get("/", response_model=CV)
def get_user_cv(
        applicant_id: str,
        token_data: TokenData = Depends(get_current_user),
        db_session=Depends(db_service.get_db)
):
    return load_user_cv(applicant_id=applicant_id, db=db_session)
