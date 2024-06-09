from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse

from app.core.config import settings
from app.core.db import db_service
from app.services.user.schemas import UserInDB, UserSession
from app.utils.iam_utils import CASDOOR_SDK as sdk, get_user_from_session

router = APIRouter()


@router.get("/auth")
async def auth(state: str = 'docs'):
    return RedirectResponse(
        url=f'{settings.CASDOOR_HOSTNAME}/login/oauth/authorize?client_id={sdk.client_id}&response_type=code&redirect_uri={settings.API_BASE_URL}/user/login/&scope=read&state={state}')


@router.get("/me")
async def me(request: Request, user=Depends(get_user_from_session)) -> UserInDB:
    return UserInDB.model_validate((sdk.get_user(user['name'])).__dict__)


@router.get("/login", include_in_schema=False)
async def login(request: Request):
    code = request.query_params.get('code')
    state = request.query_params.get('state')
    token = sdk.get_oauth_token(code)
    access_token = token.get("access_token")
    user = sdk.parse_jwt_token(access_token)
    if state == 'docs':
        response = RedirectResponse(url=f'{settings.API_BASE_URL}/docs')
        request.session["casdoorUser"] = user
        return response
    return token


@router.post("/logout", response_class=JSONResponse)
async def logout(request: Request):
    try:
        del request.session["casdoorUser"]
        return {"status": "ok"}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')



