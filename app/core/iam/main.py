import functools

import httpx
from casdoor import CasdoorSDK
from fastapi import Request, HTTPException
from requests import PreparedRequest
from starlette import status
from structlog import get_logger

from app.core.config import settings
from app.core.exceptions import ServerError
from app.core.iam.secrets import certificate
from app.core.iam.schemas import IAMUser

logger = get_logger(__name__)


class IAM:
    sdk: CasdoorSDK
    session_name: str = "casdoorUser"
    iam_endpoint: str = settings.IAM_HOSTNAME

    def __init__(self):
        self.iam_endpoint = str(settings.IAM_HOSTNAME)
        if self.iam_endpoint[-1] == '/':
            self.iam_endpoint = self.iam_endpoint[:-1]
        self.sdk = CasdoorSDK(
            endpoint=self.iam_endpoint,
            client_id=settings.IAM_CLIENT_ID,
            client_secret=settings.IAM_CLIENT_SECRET,
            certificate=certificate,
            org_name=settings.IAM_ORGANIZATION_ID,
            application_name=settings.IAM_APPLICATION_ID,
            front_endpoint=self.iam_endpoint
        )

    def get_login_url(self, redirect):
        redirect_url = settings.IAM_REDIRECT_URI
        req = PreparedRequest()
        if redirect:
            req.prepare_url(str(redirect_url), {"redirect": str(redirect)})
        else:
            req.url = str(redirect_url)
        return self.sdk.get_auth_link(redirect_uri=str(req.url))

    def get_user_from_session(self, request: Request):
        user = request.session.get(self.session_name)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user

    async def get_profile(self, user_id: str):
        logger.info("api request to iam_api", user_id=user_id)

        async with httpx.AsyncClient() as client:
            query = await client.get(url=f"{self.api_uri}/get-user", params={"userId": user_id})

        logger.info("api response from iam_api", httpx_status=query.status_code)

        if query.status_code != 200:
            raise ServerError(query.text)

        response_data = query.json()
        user = IAMUser.model_validate(response_data['data'])
        return user

    def get_token_by_code(self, code: str):
        return self.sdk.get_oauth_token(code=code)

    def parse_jwt(self, jwt: str):
        return self.sdk.parse_jwt_token(jwt)

    @functools.cached_property
    def token_uri(self) -> str:
        return self.iam_endpoint + "/login/oauth/access_token"

    @functools.cached_property
    def authorize_uri(self) -> str:
        return self.iam_endpoint + "/login/oauth/authorize"

    @functools.cached_property
    def api_uri(self) -> str:
        return self.iam_endpoint + "/api"


iam_service = IAM()
