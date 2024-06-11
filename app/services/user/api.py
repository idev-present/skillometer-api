from typing import Optional

import httpx
from fastapi import APIRouter, Depends
from pydantic import HttpUrl
from starlette.requests import Request
from starlette.responses import RedirectResponse
from structlog import get_logger

from app.core.config import settings
from app.core.db import db_service
from app.core.iam.main import iam_service
from app.services.user.crud import get_or_create_from_token
from app.services.user.middlewares import get_current_user
from app.core.iam.schemas import TokenData, TokenResponse, IAMUser

router = APIRouter()

logger = get_logger(__name__)


@router.get("/auth/login", include_in_schema=False)
async def auth(redirect: Optional[str] = None):
    target_url = iam_service.get_login_url(redirect)
    return RedirectResponse(target_url)


@router.get("/auth/callback", response_model=TokenResponse, include_in_schema=False)
async def auth_callback(code: str, redirect: Optional[str] = None):
    token = iam_service.get_token_by_code(code)
    access_token = token.get("access_token")
    if redirect == 'swagger':
        base_url = HttpUrl(url=f"{settings.IAM_REDIRECT_URI}")
        target_url = f"{base_url.scheme}://{base_url.host}{f':{base_url.port}' if base_url.port else ''}{settings.API_PREFIX}/docs"
        response = RedirectResponse(url=target_url)
        response.set_cookie('skillometer_access_token', access_token)
        return response
    return token


@router.post("/auth/callback", response_model=TokenResponse)
async def auth_callback(code: str):
    token = iam_service.get_token_by_code(code)
    return token


@router.get("/me", response_model=IAMUser)
async def me(token_data: TokenData = Depends(get_current_user)):
    iam_user = iam_service.get_profile(token_data.id)
    return iam_user


@router.get("/profile")
async def profile(token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    user = await get_or_create_from_token(token_data=token_data, db=db_session)
    return user


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
        res = httpx.post(
            f"https://career.habr.com/integrations/oauth/token?client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code&code={authorization_code}")
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
