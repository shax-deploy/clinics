# app/crud/user.py
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

# Foydalanuvchi uchun maxsus CRUD klassi
class CRUDUser(CRUDBase[User, UserCreate, UserResponse]):
    def get_user_by_username(self, db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

# CRUDUser obyektini yaratish
user_crud = CRUDUser(User)