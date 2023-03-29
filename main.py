from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from mangum import Mangum

from router.api_router import api_router
from config.config import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

handler = Mangum(app)
