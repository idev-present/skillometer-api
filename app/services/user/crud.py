from sqlalchemy.exc import DBAPIError
from structlog import get_logger

from app.core.exceptions import NotFoundError, ValidationError
from app.core.iam.main import iam_service
from app.core.iam.schemas import TokenData, IAMUser
from app.services.user.db_models import UserDBModel
from app.services.user.schemas import User

logger = get_logger(__name__)


async def get_or_create_from_token(token_data: TokenData, db):
    user_id = token_data.id
    logger.info("try find user in db", user_id=user_id)
    user_db_model = await UserDBModel.get(item_id=user_id, db=db)
    if not user_db_model:
        logger.info("user not found, try get profile from api", user_id=user_id)
        # TODO(ilya.zhuravlev): check expternal_api errors
        iam_user: IAMUser = await iam_service.get_profile(token_data.id)
        if not iam_user:
            raise NotFoundError(message="User from api not found")
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
            created_at=iam_user.created_at,
            updated_at=iam_user.updated_at,
            deleted_at=iam_user.deleted_at,
        )
        try:
            user_db_model = await UserDBModel.create(db=db, form=user_form)
        except DBAPIError as e:
            raise e
        # TODO(ilya.zhuravlev): check unuque constraint
    return user_db_model
