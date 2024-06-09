from typing import Optional

import httpx
import requests
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from structlog import get_logger

from app.core.config import settings
from app.core.db import db_service
from app.services.user.schemas import UserInDB, UserSession
from app.utils.iam_utils import CASDOOR_SDK as sdk, get_user_from_session

router = APIRouter()

logger = get_logger(__name__)


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


@router.get("/oauth/habr/", include_in_schema=False)
async def oauth_authorize(request: Request):
    if "error" in request.query_params:
        logger.error("### error habr oauth")
        logger.error(request.query_params["error"])
        return {"status": "error"}
    if "authorization_code" in request.query_params:
        client_id = "25eb730f2b7a659ee7e70a1f2da5b6aa694c3f8d263d16314cadde2880492d61"
        client_secret = "4713b17842d4676e91a9352126800c87489731a64077cfc8c4775c5e8fbed793"
        authorization_code = request.query_params["authorization_code"]
        redirect_uri = "https://skillometer.idev-present.com/vacancies"
        res = httpx.post(f"https://career.habr.com/integrations/oauth/token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code&code={authorization_code}")
        if res.status_code == 200:
            logger.info("### habr oauth ok")
            logger.info(res.json())
            return res.json()
        else:
            logger.error("### habr oauth error")
            logger.error(res.status_code)
            logger.error(res.json())
            return {"status": "error"}
    logger.error("### bad request")
    return request.query_params