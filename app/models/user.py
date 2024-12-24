# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    reception = "reception"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.reception)
    created_appointments = relationship("Appointment", back_populates="created_by")

    @classmethod
    def verify_user(cls, db: Session, email: str):
        return db.query(cls).filter(cls.email == email).first()
    

    
