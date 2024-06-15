from operator import and_
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from structlog import get_logger

from app.services.applicant.db_models import ApplicantDBModel
from app.services.user.db_models import UserDBModel

logger = get_logger(__name__)


def load_user_cv(applicant_id: str, db):
    stmt = (
        select(ApplicantDBModel)
        .options(
            joinedload(ApplicantDBModel.xp),
            joinedload(ApplicantDBModel.education),
            joinedload(ApplicantDBModel.user),
        )
        .where(
            and_(
                ApplicantDBModel.id == applicant_id,
                ApplicantDBModel.user.has(UserDBModel.role == 'applicant')
            )
        )
    )

    result = db.execute(stmt)
    applicant = result.scalars().first()
    user_data = {
        **applicant.__dict__,
        "login": applicant.user.login,
        "avatar": applicant.user.avatar,
        "phone": applicant.user.phone,
        "email": applicant.user.email,
        "gender": applicant.user.gender,
        "bio": applicant.user.bio,
    }
    return user_data
