
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List

from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserResponse, UserVerify, UserLogin, UserUpdate
from app.database import get_db
from app.models.user import User
from app.core.auth import create_access_token, verify_password, hash_password, create_refresh_token
from app.core.dependencies import get_current_user, get_current_admin_user
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/getToken")



@router.post("/getToken")
def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
    user_in_db = user_crud.get_user_by_username(db=db, username=user.username)
    if not user_in_db or not verify_password(user.password, user_in_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user_in_db.email})
    refresh_token = create_refresh_token(data={"sub": user_in_db.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }



# Joriy foydalanuvchini olish endpointi
@router.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: UserVerify = Depends(get_current_user)):
    return current_user

# Yangi foydalanuvchi yaratish
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Foydalanuvchi nomi tekshiriladi
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    # Email tekshiriladi
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    if db.query(User).filter(User.phone == user.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone already registered",
        )

    if not user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required",
        )
    
    hashed_password = hash_password(user.password)
    user.password = hashed_password

    # Foydalanuvchi yaratiladi
    return user_crud.create(db=db, obj_in=user)

# Foydalanuvchini ID orqali olish
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = user_crud.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    return db.query(User).offset(skip).limit(limit).all()


@router.put("/{id}", response_model=UserResponse)
@router.patch("/{id}", response_model=UserResponse)
def update_user(
    id: int,
    user: UserUpdate,  # PATCH uchun UserUpdate ishlatiladi
    request: Request,
    db: Session = Depends(get_db)
):
    db_user = user_crud.get(db=db, id=id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if request.method == "PUT":
        updated_data = user.dict()
        for key, value in updated_data.items():
            setattr(db_user, key, value)
    elif request.method == "PATCH":
        updated_data = user.dict(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# Foydalanuvchini o'chirish
@router.delete("/{id}", response_model=UserResponse)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = user_crud.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.delete(db=db, id=id)
    return user
