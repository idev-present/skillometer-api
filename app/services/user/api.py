from typing import List, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from structlog import get_logger

from app.core.config import settings
from app.core.iam.main import iam_service
from app.services.user.schemas import UserInDB

router = APIRouter()

logger = get_logger(__name__)


@router.get("/auth/login")
async def auth(redirect: Optional[str] = None):
    target_url = iam_service.get_login_url(redirect)
    return RedirectResponse(target_url)


@router.get("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get('code')
    redirect = request.query_params.get('redirect')
    token = iam_service.get_token_by_code(code)
    access_token = token.get("access_token")
    if redirect == 'swagger':
        base_url = HttpUrl(url=f"{settings.IAM_REDIRECT_URI}")
        target_url = f"{base_url.scheme}://{base_url.host}{f':{base_url.port}' if base_url.port else ''}{settings.API_PREFIX}/docs"
        response = RedirectResponse(url=target_url)
        response.set_cookie('skillometer_access_token', access_token)
        return response
    return token


@router.post("/auth/callback")
async def auth_callback(request: Request):
    code = request.query_params.get('code')
    token = iam_service.get_token_by_code(code)
    access_token = token.get("access_token")
    session = iam_service.parse_jwt(access_token)
    request.session[iam_service.session_name] = session
    return token


@router.get("/me")
async def me(user=Depends(iam_service.get_user_from_session)) -> UserInDB:
    user_data = iam_service.get_profile(user_id=user['name'])
    if user.get('roles') and isinstance(user.get('roles'), list):
        if isinstance(user['roles'][0], dict):
            user_role = user['roles'][0].get('name')
    result = UserInDB.model_validate(user_data.__dict__)
    result.role = user_role if user_role else None
    return result


@router.post("/logout")
async def logout(request: Request):
    try:
        del request.session[iam_service.session_name]
        return {"status": "ok"}
    except KeyError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')


@router.get("/")
async def list_users(_: dict = Depends(iam_service.get_user_from_session)) -> List[UserInDB]:
    return iam_service.sdk.get_users()


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
