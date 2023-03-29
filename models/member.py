import datetime
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import List, Optional
from config.db import Base


class Member(Base):
    __tablename__ = "t_user"
    user_id = Column(String, primary_key=True)
    user_name = Column(String)
    password = Column(String)
    email = Column(String)
    role = Column(String)
    birth = Column(String)
    gender = Column(String)
    reflash_token = Column(String)
    reg_date = Column(Date)
    upt_date = Column(Date)


class MemberBase(BaseModel):
    user_id: str
    user_name: str
    password: str
    email: str
    role: str
    birth: str
    gender: str
    reflash_token: str
    reg_date: datetime.date
    upt_date: datetime.date


class MemberCreate(MemberBase):
    pass


class MemberUpdate(MemberBase):
    pass


class MemberOut(MemberBase):
    user_id: str

    class Config:
        orm_mode = True
