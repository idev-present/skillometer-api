from casdoor import CasdoorSDK
from fastapi import Request, HTTPException
from requests import PreparedRequest
from starlette import status

from app.core.config import settings
from app.core.iam.secrets import certificate


class IAM:
    sdk: CasdoorSDK
    session_name: str = "casdoorUser"

    def __init__(self):
        iam_endpoint = str(settings.IAM_HOSTNAME)
        if iam_endpoint[-1] == '/':
            iam_endpoint = iam_endpoint[:-1]
        self.sdk = CasdoorSDK(
            endpoint=iam_endpoint,
            client_id=settings.IAM_CLIENT_ID,
            client_secret=settings.IAM_CLIENT_SECRET,
            certificate=certificate,
            org_name=settings.IAM_ORGANIZATION_ID,
            application_name=settings.IAM_APPLICATION_ID,
            front_endpoint=iam_endpoint
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

    def get_profile(self, user_id: str):
        return self.sdk.get_user(user_id=user_id)

    def get_token_by_code(self, code: str):
        return self.sdk.get_oauth_token(code=code)

    def parse_jwt(self, jwt: str):
        return self.sdk.parse_jwt_token(jwt)


iam_service = IAM()
