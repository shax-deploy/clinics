from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User  # Modelni to'g'ri import qilganingizga ishonch hosil qiling
from app.core.auth import decode_access_token  # Tokenni dekodlash funksiyasini to'g'ri import qiling
from app.database import get_db

# Token olish uchun URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/getToken")


# Foydalanuvchini autentifikatsiya qilish
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = decode_access_token(token=token)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = User.verify_user(db=db, email=email)
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception

# Admin huquqlarini tekshirish
def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.role=="admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an Admin.",
        )
    return current_user

def get_current_reception_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.role=="reception":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be an Reception.",
        )
    return current_user
