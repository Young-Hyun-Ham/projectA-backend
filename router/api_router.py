from fastapi import APIRouter

from router import board, member, token, lotto, login

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["로그인"])
api_router.include_router(board.router, prefix="/board", tags=["게시판"])
api_router.include_router(member.router, prefix="/member", tags=["맴버"])
api_router.include_router(token.router, prefix="/token", tags=["토큰"])
api_router.include_router(lotto.router, prefix="/lotto", tags=["로또"])
