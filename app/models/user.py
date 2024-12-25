# app/models/user.py
from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
import enum
import re
from sqlalchemy.orm import validates


class RoleEnum(str, enum.Enum):
    admin = "admin"
    reception = "reception"
    doctor = "doctor"  # Doktorlar uchun yangi rol


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String)
    phone = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.reception) 

    # Bog'lanish
    created_appointments = relationship("Appointment", back_populates="created_by")  # Reception tomonidan yaratilgan appointmentlar
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)

    @validates("phone")
    def validate_phone(self, key, value):
        """
        Telefon raqamini tekshirish.
        Raqam faqat 9 ta raqamdan iborat bo'lishi kerak.
        """
        if not re.fullmatch(r"^\d{9}$", value):
            raise ValueError("Phone number must be exactly 9 digits.")
        return value

    
