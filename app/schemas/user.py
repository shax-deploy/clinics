# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    reception = "reception"
    doctor = "doctor"


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    phone: str = Field(..., pattern=r"^\d{9}$")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: RoleEnum = RoleEnum.reception


class UserCreate(UserBase):
    password: str = Field(..., min_length=4)
#     password: str = Field(
#     ...,
#     min_length=8,
#     regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$",
#     description="Kamida 8 belgidan iborat, katta va kichik harflar hamda son bo'lishi kerak"
# )
    # class Config:
    #     orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\d{9}$")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role: RoleEnum

    @property
    def is_admin(self):
        return self.role == RoleEnum.admin

    class Config:
        orm_mode = True

class UserVerify(BaseModel):
    id: int
    username: str
    phone: str
    first_name: Optional[str] = None

    class Config:
        orm_mode = True



class UserLogin(BaseModel):
    username: str
    password: str
