from fastapi import APIRouter, Form, HTTPException, Response
from pydantic import BaseModel

from typing import Optional
import requests
import json

import config.security as security

router = APIRouter()

# KakaoTalk OAuth2 configuration
kko_client_id = "a54c2dcde69ad8892477eecfb220ab0c"
kko_client_secret = "3Xf7RifxH0n8V73EY1AVEWyt9qv1pWjq"
# 카카오 개발자 센터에서 등록한 콜백 URL
kko_redirect_uri = "http://localhost:8000/api/v1/login/kakao/callback"
kko_token_url = "https://kauth.kakao.com/oauth/token"
kko_user_url = "https://kapi.kakao.com/v2/user/me"


class User(BaseModel):
    userId: str
    userPwd: str
    username: str
    email: str
    password: str
    access_token: Optional[str] = ""


class Token(BaseModel):
    access_token: str
    reflash_token: str
    token_type: str


@router.post("/login")
def 로그인(user: User):
    if user.userId == "admin" and user.userPwd == "1234":
        access_token = security.create_access_token(subject=user.userId)
        reflash_token = security.create_reflash_token(subject=user.userId)
        return Token(access_token=access_token, reflash_token=reflash_token, token_type="bearer")
    else:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")


@router.post("/kakao/callback")
async def 카카오_로그인(code: str):
    # Get access token using authorization code
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    data = {
        "grant_type": "authorization_code",
        "client_id": kko_client_id,
        "client_secret": kko_client_secret,
        "redirect_uri": kko_redirect_uri,
        "code": code
    }
    response = requests.post(kko_token_url, headers=headers, data=data)
    print(response)
    access_token = json.loads(response.text)["access_token"]

    # Get user information using access token
    headers = {"Authorization": "Bearer {}".format(access_token)}
    response = requests.get(kko_user_url, headers=headers)
    user_info = json.loads(response.text)

    # 디비 검증?
    print(access_token)
    print(user_info)

    # Return access token
    return {"access_token": access_token}
