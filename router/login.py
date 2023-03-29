from datetime import timedelta
from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from config.config import Settings

import config.security as security

router = APIRouter()


class User(BaseModel):
    userId: str
    userPwd: str


class Token(BaseModel):
    access_token: str
    reflash_token: str
    token_type: str


@router.post("/login")
def 로그인(user: User):
    if user.userId == "admin" and user.userPwd == "1234":
        access_token = security.create_access_token(subject=user.userId)
        reflash_token = security.create_reflash_token(subject=user.userId)
        return Token({"access_token": access_token, "reflash_token": reflash_token, "token_type": "bearer"})
    else:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password")
