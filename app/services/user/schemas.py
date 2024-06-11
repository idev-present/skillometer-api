from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from app.utils.api_utils import str2datetime


class CasdoorUser(BaseModel):
    """
    example
    {
		"owner": "org_woai_test",
		"name": "test_user",
		"createdTime": "2023-03-30T18:38:25+08:00",
		"updatedTime": "",
		"id": "5cf501cc-d7d0-4975-89d3-25b4d3b486c7",
		"type": "normal-user",
		"password": "",
		"passwordSalt": "",
		"displayName": "测试用户",
		"firstName": "",
		"lastName": "",
		"avatar": "https://cdn.casbin.org/img/casbin.svg",
		"permanentAvatar": "",
		"email": "i@iaside.com",
		"emailVerified": false,
		"phone": "13120165229",
		"location": "",
		"address": [],
		"affiliation": "Example Inc.",
		"title": "",
		"idCardType": "",
		"idCard": "",
		"homepage": "",
		"bio": "",
		"region": "",
		"language": "",
		"gender": "",
		"birthday": "",
		"education": "",
		"score": 0,
		"karma": 0,
		"ranking": 2,
		"isDefaultAvatar": false,
		"isOnline": false,
		"isAdmin": false,
		"isGlobalAdmin": false,
		"isForbidden": false,
		"isDeleted": false,
		"signupApplication": "application_woai_test",
		"hash": "",
		"preHash": "",
		"createdIp": "",
		"lastSigninTime": "",
		"lastSigninIp": "",
		"ldap": "",
		"properties": {},
		"roles": [],
		"permissions": [],
		"lastSigninWrongTime": "",
		"signinWrongTimes": 0,
		"tokenType": "access-token",
		"tag": "staff",
		"iss": "https://casdoor.test.sinkstars.com",
		"sub": "5cf501cc-d7d0-4975-89d3-25b4d3b486c7",
		"aud": [
			"97c018a6692f932ab6d1"
		],
		"exp": 1680261803,
		"nbf": 1680175403,
		"iat": 1680175403,
		"jti": "admin/64e60a04-49ca-4452-beac-c445f924bac5"
	}
    """
    id: str
    name: str
    displayName: str
    firstName: str
    lastName: str
    email: str
    emailVerified: bool
    phone: str

    avatar: str
    permanentAvatar: str
    isDefaultAvatar: bool

    owner: str
    signupApplication: str

    type: str
    roles: list[dict]
    permissions: list[str]
    tag: str

    isOnline: bool
    isAdmin: bool
    isForbidden: bool
    isDeleted: bool

    createdTime: datetime | None
    updatedTime: datetime | None

    @staticmethod
    def from_token_dict(token_dict: dict):
        token_dict['createdTime'] = str2datetime(token_dict['createdTime'])
        token_dict['updatedTime'] = str2datetime(token_dict['updatedTime'])
        # if token_dict.get('exp'):
        #     token_dict['exp'] = datetime.fromtimestamp(token_dict['exp'])
        return CasdoorUser(**token_dict)


class BaseUser(BaseModel):
    email: Optional[str]
    name: Optional[str]
    phone: Optional[str]


class UserInDB(BaseUser):
    id: str
    role: Optional[str] = Field(None)
    avatar: Optional[str]
    created_time: datetime = Field(alias='createdTime')


class UserSession(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
