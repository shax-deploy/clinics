from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User  # User modelini import qilish
from app.schemas.user import UserVerify

# Parol hashing uchun passlib konteksti
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token yaratish funksiyasi
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT access token yaratadi.
    :param data: Token ichiga joylanadigan foydalanuvchi ma'lumotlari
    :param expires_delta: Token amal qilish muddati
    :return: Yaratilgan JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))  # Default 15 daqiqa
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))  # 7 kun
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# JWT tokenni dekodlash funksiyasi
def decode_access_token(token: str) -> dict:
    """
    JWT tokenni dekodlash.
    :param token: Tekshirilayotgan JWT token
    :return: Token ichidagi foydalanuvchi ma'lumotlari
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Token orqali foydalanuvchini tekshirish
def get_user_from_token(token: str) -> UserVerify:
    """
    Token orqali foydalanuvchi ma'lumotlarini olish.
    :param token: JWT token
    :return: Foydalanuvchi (UserVerify schema)
    """
    payload = decode_access_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = User.verify_user(email=email)  # User modelida `verify_user` metodi kerak
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user

# Parolni tekshirish funksiyasi
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Foydalanuvchi tomonidan kiritilgan parolni saqlangan hashed parol bilan taqqoslash.
    :param plain_password: Foydalanuvchi tomonidan kiritilgan parol
    :param hashed_password: Ma'lumotlar bazasida saqlangan hashed parol
    :return: True agar parol mos bo'lsa; False aks holda
    """
    return pwd_context.verify(plain_password, hashed_password)

# Parolni hash qilish funksiyasi
def hash_password(password: str) -> str:
    """
    Parolni hash qilish.
    :param password: Oddiy parol
    :return: Hashed parol
    """
    return pwd_context.hash(password)
