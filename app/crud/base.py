from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, Any, Dict
from app.models.user import User
from app.models.clinics import Doctor
from app.schemas.clinics import DoctorCreate, DoctorUpdate

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType):
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_patient(self, db: Session, obj_in: dict):
        db_obj = self.model(**obj_in)  # obj_in.dict() emas, chunki obj_in allaqachon dict
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType):
        obj_data = obj_in.dict(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


class CRUDDoctor(CRUDBase[Doctor, DoctorCreate, DoctorUpdate]):
    """
    Doktor uchun maxsus CRUD.
    """
    def create_with_doctor(self, db: Session, user_data: dict, doctor_data: dict):
        """
        Doktor va unga tegishli foydalanuvchini yaratish.
        """
        # Foydalanuvchini yaratish
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)

        # Doktorni yaratish va foydalanuvchi bilan bog'lash
        doctor = self.model(id=user.id, **doctor_data)
        db.add(doctor)
        db.commit()
        db.refresh(doctor)

        return doctor
    
    # def update_with_doctor(self, db: Session, doctor_id: int, doctor_data: DoctorUpdate):
    #     db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        
    #     if not db_doctor:
    #         raise HTTPException(status_code=404, detail="Doctor not found")

    #     # Yangilanishlarni qo'llash
    #     for key, value in doctor_data.dict(exclude_unset=True).items():
    #         setattr(db_doctor, key, value)

    #     # O'zgarishlarni bazaga saqlash
    #     db.commit()
    #     db.refresh(db_doctor)
    #     return db_doctor
    

    def update_patch_with_doctor(self, db: Session, doctor_id: int, doctor_data: DoctorUpdate):
        # Doktorni olish
        db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Doktorning foydalanuvchisini olish
        db_user = db_doctor.user

        # Doktor uchun yangilanishlarni qo'llash
        doctor_fields = {key: value for key, value in doctor_data.dict(exclude_unset=True).items() if hasattr(Doctor, key)}
        for key, value in doctor_fields.items():
            setattr(db_doctor, key, value)

        # Foydalanuvchi uchun yangilanishlarni qo'llash
        user_fields = {key: value for key, value in doctor_data.dict(exclude_unset=True).items() if hasattr(User, key)}
        for key, value in user_fields.items():
            setattr(db_user, key, value)

        # O'zgarishlarni bazaga saqlash
        db.commit()
        db.refresh(db_doctor)
        return db_doctor

    def update_put_with_doctor(self, db: Session, doctor_id: int, doctor_data: DoctorCreate):
        # Doktorni olish
        db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Doktorning foydalanuvchisini olish
        db_user = db_doctor.user

        # Doktor uchun yangilanishlarni qo'llash
        doctor_fields = {key: value for key, value in doctor_data.dict().items() if hasattr(Doctor, key)}
        for key, value in doctor_fields.items():
            setattr(db_doctor, key, value)

        # Foydalanuvchi uchun yangilanishlarni qo'llash
        user_fields = {key: value for key, value in doctor_data.dict().items() if hasattr(User, key)}
        for key, value in user_fields.items():
            setattr(db_user, key, value)

        # O'zgarishlarni bazaga saqlash
        db.commit()
        db.refresh(db_doctor)
        return db_doctor