import os
import json

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')
secrets = json.loads(open(SECRET_FILE).read())
DB = secrets["DB"]
ENV = secrets["ENV"]


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = f"{ENV['secretkey']}"
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 1 days = 1 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    REFLASH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1

    # Database connection
    HOST: str = f"{DB['host']}"
    PORT: int = f"{DB['port']}"
    USERNAME: str = f"{DB['user']}"
    PASSWORD: str = f"{DB['password']}"
    DATABASE: str = f"{DB['database']}"
    # FIRST_SUPERUSER_EMAIL: EmailStr = os.getenv('FIRST_SUPERUSER_EMAIL')
    # FIRST_SUPERUSER_PASSWORD: str = os.getenv('FIRST_SUPERUSER_PASSWORD')
    SQLALCHEMY_DATABASE_URL = f'mariadb+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

    class Config:
        case_sensitive = True


settings = Settings()
