from lib2to3.pytree import Base
from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from config.db import Base
from typing import Optional


class lottoTable(Base):
    __tablename__ = "t_lotto"

    no = Column(Integer, primary_key=True, index=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    num3 = Column(Integer, nullable=False)
    num4 = Column(Integer, nullable=False)
    num5 = Column(Integer, nullable=False)
    num6 = Column(Integer, nullable=False)
    bonus = Column(Integer, nullable=False)


class lotto(BaseModel):
    no: Optional[int] = 0
    num1: int
    num2: int
    num3: int
    num4: int
    num5: int
    num6: int
    bonus: Optional[int] = 0


class lottoOut(BaseModel):
    statusCode: int
    data: lotto
    resultCode: str
    resultMessage: str
