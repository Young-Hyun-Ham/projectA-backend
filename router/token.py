from fastapi import APIRouter, Depends, Body, HTTPException

import config.security as security

router = APIRouter()


@router.get("/getToken")
def 토큰생성하기():
    access_token = security.create_access_token(subject="test")
    return {"access_token": access_token}
