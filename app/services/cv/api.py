from operator import and_

from fastapi import APIRouter, Depends
from sqlalchemy import select, join
from sqlalchemy.orm import selectinload, joinedload
from structlog import get_logger

from app.core.db import db_service
from app.core.iam.schemas import TokenData
from app.services.applicant.db_models import ApplicantDBModel
from app.services.cv.schemas import CV
from app.services.user.db_models import UserDBModel
from app.services.user.middlewares import get_current_user

router = APIRouter()

logger = get_logger(__name__)


@router.get("/", response_model=CV)
async def get_user_cv(session=Depends(db_service.get_db)):
    stmt = (
        select(ApplicantDBModel)
        .options(
            joinedload(ApplicantDBModel.xp),
            joinedload(ApplicantDBModel.education),
            joinedload(ApplicantDBModel.user),
        )
        .where(
            and_(
                ApplicantDBModel.id == 'basta_zdes_2006',
                ApplicantDBModel.user.has(UserDBModel.role == 'applicant')
            )
        )
    )

    result = await session.execute(stmt)
    applicant = result.scalars().first()
    user_data = {
        **applicant.__dict__,
        "login": applicant.user.login,
        "avatar": applicant.user.avatar,
        "phone": applicant.user.phone,
        "email": applicant.user.email,
        "bio": applicant.user.bio,
    }
    return user_data