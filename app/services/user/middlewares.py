from typing import Annotated

from fastapi import Depends, HTTPException
from starlette import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError

from app.core.iam.main import iam_service
from app.core.iam.schemas import TokenData

user_auth_scheme = HTTPBearer()


async def parse_user_token(credentials: HTTPAuthorizationCredentials = Depends(user_auth_scheme)) -> TokenData:
    if credentials.scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme")
    token: str = credentials.credentials
    try:
        user_dict = iam_service.parse_jwt(token)
        if not user_dict:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Empty token")
        user = TokenData(**user_dict)
        return user
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def get_current_user(user: Annotated[TokenData, Depends(parse_user_token)]):
    if user.isDeleted or user.isForbidden:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to access this resource")
    return user
