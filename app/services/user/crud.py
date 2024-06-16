import arrow
from sqlalchemy import sql
from sqlalchemy.exc import DBAPIError
from structlog import get_logger
from fastapi import HTTPException
from starlette import status
from app.core.iam.main import iam_service
from app.core.iam.schemas import TokenData, IAMUser
from app.services.applicant.db_models import ApplicantDBModel
from app.services.applicant.schemas import Applicant
from app.services.user.db_models import UserDBModel
from app.services.user.schemas import User

logger = get_logger(__name__)


async def get_or_create_user_from_token(token_data: TokenData, db):
    user_id = token_data.id
    logger.info("try find user in db", user_id=user_id)
    user_db_model = UserDBModel.get(item_id=user_id, db=db)
    applicant = db.execute(sql.select(ApplicantDBModel).where(ApplicantDBModel.user_id == user_id)).scalars().first()
    if not user_db_model:
        logger.info("user not found, try get profile from api", user_id=user_id)
        # TODO(ilya.zhuravlev): check external_api errors
        iam_user: IAMUser = await iam_service.get_profile(token_data.id)
        if not iam_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User from api not found")
        logger.info("mapping user and iam_user fields", iam_user=iam_user.id)
        user_form = User(
            id=iam_user.id,
            login=iam_user.name,
            avatar=iam_user.avatar,
            gender=iam_user.gender,
            first_name=iam_user.firstName,
            last_name=iam_user.lastName,
            full_name=iam_user.displayName,
            birthday=iam_user.birthday,
            bio=iam_user.bio,
            role=iam_user.role,
            email=iam_user.email,
            country_code=iam_user.countryCode,
            phone=iam_user.phone,
            city=iam_user.location,
            has_applicant=True if applicant else False,
            created_at=iam_user.created_at,
            updated_at=iam_user.updated_at,
            deleted_at=iam_user.deleted_at,
        )
        try:
            user_db_model = UserDBModel.create(db=db, form=user_form)
        except DBAPIError as e:
            raise e
        # TODO(ilya.zhuravlev): check unique constraint
    result = User.model_validate(user_db_model.__dict__)
    result.has_applicant = True if applicant else False
    return result


def get_or_create_applicant_from_token(token_data: TokenData, db):
    applicant = ApplicantDBModel.get(item_id=token_data.name, db=db)
    if not applicant:
        user_db_model = UserDBModel.get(item_id=token_data.id, db=db)
        if not user_db_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        applicant = ApplicantDBModel(
            id=user_db_model.login,
            user_id=user_db_model.id,
            title=f"{user_db_model.first_name} {user_db_model.last_name}",
        )
        if user_db_model.birthday:
            birthday_date = arrow.get(user_db_model.birthday)
            now = arrow.now()
            age = now.year - birthday_date.year
            applicant.age = age

        db.add(applicant)
        db.commit()
        db.refresh(applicant)
    return applicant
