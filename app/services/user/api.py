from typing import Optional, List

import httpx
from fastapi import APIRouter, Depends, Response
from pydantic import HttpUrl
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from structlog import get_logger

from app.core.config import settings
from app.core.db import db_service
from app.core.iam.main import iam_service
from app.services.applicant.db_models import ApplicantDBModel, ApplicantXPDBModel, ApplicantEducationDBModel
from app.services.applicant.schemas import ApplicantUpdateForm, ApplicantXP, ApplicantXPForm, ApplicantXPUpdateForm, \
    ApplicantEducationForm, ApplicantEducation, ApplicantEducationUpdateForm, Applicant
from app.services.cv.main import load_user_cv
from app.services.cv.schemas import CV
from app.services.reply.db_models import ReplyDBModel
from app.services.reply.schemas import Reply, ReplyDBModelFilters
from app.services.user.crud import get_or_create_user_from_token, get_or_create_applicant_from_token
from app.services.user.db_models import UserDBModel
from app.services.user.middlewares import get_current_user
from app.core.iam.schemas import TokenData, TokenResponse
from app.services.user.schemas import User, UserUpdateForm, UserContacts

router = APIRouter()

logger = get_logger(__name__)


@router.get("/auth/login", include_in_schema=False)
def auth(redirect: Optional[str] = None):
    target_url = iam_service.get_login_url(redirect)
    return RedirectResponse(target_url)


@router.get("/auth/callback", response_model=TokenResponse, include_in_schema=False)
def redirect_auth_callback(code: str, redirect: Optional[str] = None):
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
def auth_callback(code: str):
    token = iam_service.get_token_by_code(code)
    return token


@router.get("/profile", response_model=User)
async def get_user_profile(token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    user = await get_or_create_user_from_token(token_data=token_data, db=db_session)
    return user


@router.put("/profile", response_model=User)
def update_user_profile(form: UserUpdateForm, token_data: TokenData = Depends(get_current_user),
                              db_session=Depends(db_service.get_db)) -> User:
    res = UserDBModel.update(form=form, item_id=token_data.id, db=db_session)
    return res


@router.get("/applicant_info", response_model=Applicant)
def get_applicant_info(token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    res = get_or_create_applicant_from_token(token_data=token_data, db=db_session)
    return res


@router.put("/applicant_info", response_model=Applicant)
def update_applicant_info(form: ApplicantUpdateForm, token_data: TokenData = Depends(get_current_user),
                                db_session=Depends(db_service.get_db)):
    res = ApplicantDBModel.update(item_id=token_data.name, form=form, db=db_session)
    return res


@router.get("/contacts", response_model=UserContacts)
def get_contacts(token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    res = UserDBModel.get(item_id=token_data.id, db=db_session)
    return res


@router.put("/contacts", response_model=UserContacts)
def update_contacts(form: UserContacts, token_data: TokenData = Depends(get_current_user),
                          db_session=Depends(db_service.get_db)):
    res = UserDBModel.update(item_id=token_data.id, form=form, db=db_session)
    return res


@router.post('/education', response_model=ApplicantEducation)
def create_education_info(form: ApplicantEducationForm, token_data: TokenData = Depends(get_current_user),
                                db_session=Depends(db_service.get_db)):
    res = ApplicantEducationDBModel.create(form=form, parent_id=token_data.name, db=db_session)
    return res


@router.get('/education', response_model=List[ApplicantEducation])
def get_education_info(token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    res = ApplicantEducationDBModel.get_list(parent_id=token_data.name, db=db_session)
    return res


@router.put('/education/{education_item_id}', response_model=ApplicantEducation)
def update_education_info(education_item_id: str, form: ApplicantEducationUpdateForm,
                                token_data: TokenData = Depends(get_current_user),
                                db_session=Depends(db_service.get_db)):
    res = ApplicantEducationDBModel.update(form=form, item_id=education_item_id, db=db_session)
    return res


@router.delete('/education/{education_item_id}')
def delete_education_info(education_item_id: str,
                                token_data: TokenData = Depends(get_current_user),
                                db_session=Depends(db_service.get_db)):
    res = ApplicantEducationDBModel.delete(item_id=education_item_id, db=db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/work_xp", response_model=List[ApplicantXP])
def get_work_xp_list(token_data: TokenData = Depends(get_current_user), db_session=Depends(db_service.get_db)):
    res = ApplicantXPDBModel.get_list(parent_id=token_data.name, db=db_session)
    return res


@router.post("/work_xp", response_model=ApplicantXPForm)
def create_work_xp(form: ApplicantXPForm, token_data: TokenData = Depends(get_current_user),
                         db_session=Depends(db_service.get_db)):
    res = ApplicantXPDBModel.create(form=form, parent_id=token_data.name, db=db_session)
    return res


@router.put("/work_xp/{xp_id}", response_model=ApplicantXPForm)
def update_work_xp(xp_id: str, form: ApplicantXPUpdateForm, token_data: TokenData = Depends(get_current_user),
                         db_session=Depends(db_service.get_db)):
    res = ApplicantXPDBModel.update(item_id=xp_id, form=form, db=db_session)
    return res


@router.delete("/work_xp/{xp_id}")
def delete_work_xp(xp_id: str, token_data: TokenData = Depends(get_current_user),
                         db_session=Depends(db_service.get_db)):
    res = ApplicantXPDBModel.delete(item_id=xp_id, db=db_session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/cv", response_model=CV)
def get_cv(token_data=Depends(get_current_user), db_session=Depends(db_service.get_db)
                 ):
    res = load_user_cv(applicant_id=token_data.name, db=db_session)
    return res


@router.get("/reply/history", response_model=List[Reply])
def get_user_replies_history(
        token_data: TokenData = Depends(get_current_user),
        db_session=Depends(db_service.get_db)
):
    filters = ReplyDBModelFilters(applicant_id=token_data.name)
    res = ReplyDBModel.get_list(filters=filters, db=db_session)
    return res


@router.get("/oauth/habr/", include_in_schema=False)
def habr_oauth_authorize(request: Request):
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
