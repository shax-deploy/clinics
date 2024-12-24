# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str | None
    is_admin: bool

    class Config:
        orm_mode = True

class UserVerify(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    username: str
    password: str
