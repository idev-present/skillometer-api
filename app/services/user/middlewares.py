from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jwt import DecodeError

from app.core.exceptions import UnauthorizedError, ServerError, PermissionError
from app.core.iam.main import iam_service
from app.services.user.schemas import CasdoorUser


user_auth_scheme = HTTPBearer()


async def get_current_user_without_check(credentials: HTTPAuthorizationCredentials = Depends(user_auth_scheme)) -> CasdoorUser:
    if credentials.scheme != "Bearer":
        raise UnauthorizedError(message="Invalid token scheme")
    token: str = credentials.credentials
    try:
        user_dict = iam_service.parse_jwt(token)
        if not user_dict:
            raise UnauthorizedError(message="Empty token")
        user = CasdoorUser.from_token_dict(user_dict)
        return user
    except DecodeError:
        raise UnauthorizedError(message="Token is invalid")
    except Exception as e:
        raise ServerError(message=str(e))


async def get_current_user(user: Annotated[CasdoorUser, Depends(get_current_user_without_check)]):
    if user.isDeleted or user.isForbidden:
        raise PermissionError(message="You are not allowed to access this resource")
    return user