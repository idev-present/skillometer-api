import os

from casdoor import AsyncCasdoorSDK, CasdoorSDK
from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

from app.core.config import settings

certificate = '''-----BEGIN CERTIFICATE-----
MIIE3TCCAsWgAwIBAgIDAeJAMA0GCSqGSIb3DQEBCwUAMCgxDjAMBgNVBAoTBWFk
bWluMRYwFAYDVQQDEw1jZXJ0LWJ1aWx0LWluMB4XDTI0MDUyOTIwMDM0MFoXDTQ0
MDUyOTIwMDM0MFowKDEOMAwGA1UEChMFYWRtaW4xFjAUBgNVBAMTDWNlcnQtYnVp
bHQtaW4wggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQCoJKhJjdrxXCTj
uxYHBj3CUvZZ8gWJjHwRBbH+VCnRgQqm1ziQIZyIEuUbZ2F3iTmyHqppRba1FKY2
6fZPyS3XZXrNF2u6mnJwJyKxWtb6E4rNRCS5Sw+ikPtFSD4kACMDSEJtMzSdZRP3
PtteIpW7fF8QP0o+8sKHQ+LPh8g55VV9FTfAI4lXF0n9omMgmQ72jGNzh7vYg4wJ
ETcPweVHPRxSU5CvXPQOwCc3DDnR66t4vn2iMhSdTGgNgXRLt+0MCMuIKQWkpIvg
7gMgIofpH+/OwK6Fhkzx4hloXNd5dvGDe18WpT6mxrCTlh1GxVMYAVcMlvvvQ/bi
GiMo4NH+dWX46qBiq96yv7sTR7rZ2QDOAmL6GJbBEqVbFnwuSD9JH4ateUqvVHZT
XmM/oezt6efqWq+SLn4o9OdUd225+5U3FchjsvwANOgRtxtK4GhvplYJnHLhOsY2
2622pDZa1m/I143sYASGadTGpQQ74R3iAVI2dilSv3sQjLGFGL5plJyVYGqgAGQD
lraNboi3GWq9JlsjCHDmnxl1m5PJdscH1MEYJvD4xoqJFyUyJuVZXY/Vc9o2We84
ltGKTxdlHa6itij1xzIyahPXUgvgBwVNVtm3JGZYandFEKVZOnAlP/vS7n/sMzLK
zLTSEg8AWLzvoPsjRoqW+42NRrGYmwIDAQABoxAwDjAMBgNVHRMBAf8EAjAAMA0G
CSqGSIb3DQEBCwUAA4ICAQAg6vmHpTKRedDVSxBUGhUPjHBDLHhLMOFwxn9IlvZ7
/ONWgwUn4F5UUPvUm+GroF3ot69ZQ3j06DOMy2h8Dp6oBfUU9qixbE/fg1gSZccH
Dgb27UVTszX93jfEuvRggNVTTTyOc9gt2KfPWSoa+vI3wGXu/9jPRETIQDdUmV5m
G+6HZQAEGJqoeSix2OZUakZfLOZPkxyJOxgTifOvsND9+rZFRaiDn8jh7aP/wyle
JSp2gVDGKZ2+iP954y8sqb0jyZLvBTPzywcH2yaSrWBLtREejETT54AL6FN5XsyQ
K+cuIAwIWl/Ci5tTSoM1xuF7aDG04GKaoIDbPHxpYRgK2H+wjO8VMjdYtd4N/oUR
iVF5fgk2vgPCgAnsrgOneojoWxO1LEKciFp76XA/DGyhRuhEBmJqOCqwrqOSovG2
1bvguzkJegjVIVE4oXDmF1aVRkNnQ4iyt0mQnQAphLojbSyrtajIneilHC/PF+5f
yTgAc+HRSlqaBDl1wFfej2EZu5w3gnz8I1AvoCRc6Gxn/obWTdyqkx3lF9/mULL0
Mzr+5OYXmHUO9SUvVsTy/8JOaQcxr7DSIqtgQxfF5NlCsMwjyWUbCVQBvL0ADyzx
a6kkNI/myPxzkcH5vVLLknknOrunnonXt5AkMbGHyEf4ZqLDDMmqO4CL5S+Ik8Lf
cg==
-----END CERTIFICATE-----'''


CASDOOR_SDK = CasdoorSDK(
    endpoint=settings.CASDOOR_HOSTNAME,
    client_id='8aa124a89a76caf4e84b',
    client_secret='fa026ac3608de86085c8fe9cbac8f784ba764fd1',
    certificate=certificate,
    org_name='skillometer',
    application_name='skillometer',
)
REDIRECT_URI = settings.API_BASE_URL
SECRET_TYPE = 'filesystem'
SECRET_KEY = os.urandom(24)


async def get_user_from_session(request: Request):
    user = request.session.get("casdoorUser")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user


async def get_account(request: Request, user=Depends(get_user_from_session)):
    sdk = request.app.state.sdk
    print(user)
    return {"status": "ok", "data": sdk.get_user(user["name"])}
