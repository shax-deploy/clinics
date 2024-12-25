from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional
from app.schemas.user import UserResponse

# Doctor Schemas
class DoctorBase(BaseModel):
    specialization: str = Field(..., max_length=100)

class DoctorCreate(BaseModel):
    username: str
    phone: str = Field(..., pattern=r"^\d{9}$")
    first_name: Optional[str]
    last_name: Optional[str] = None
    password: str = Field(..., min_length=3)
    specialization: str = Field(..., max_length=100)

class DoctorUpdate(BaseModel):
    specialization: Optional[str] = Field(None, min_length=2)
    username: Optional[str] = None
    first_name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^\d{9}$")
    email: Optional[EmailStr] = None
    last_name: Optional[str] = None
    
    class Config:
        orm_mode = True

class DoctorResponse(DoctorBase):
    id: int
    specialization: Optional[str] = None
    user: UserResponse

    class Config:
        orm_mode = True


# DoctorService Schemas
class DoctorServiceBase(BaseModel):
    service_name: str
    price: float

class DoctorServiceCreate(DoctorServiceBase):
    doctor_id: int

class DoctorServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    price: Optional[float] = None

class DoctorServiceResponse(DoctorServiceBase):
    id: int
    doctor_id: int

    class Config:
        orm_mode = True


# Patient Schemas
class PatientBase(BaseModel):
    first_name: str
    phone: str = Field(..., pattern=r"^\d{9}$")
    date_of_birth: Optional[date] = None

class PatientCreate(PatientBase):
    # password: str = Field(..., min_length=3)
    # first_name: Optional[str]
    last_name: Optional[str] = None
    # phone: Optional[str] = Field(..., pattern=r"^\d{9}$")
    email: Optional[EmailStr] = None
    # date_of_birth: Optional[date] = None

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = Field(None, pattern=r"^\d{9}$")
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None

class PatientResponse(PatientBase):
    id: int
    last_name: Optional[str] = None
    class Config:
        orm_mode = True


# Appointment Schemas
class AppointmentBase(BaseModel):
    appointment_date: date
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int
    service_id: int

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    service_id: int

    class Config:
        orm_mode = True


# PatientHistory Schemas
class PatientHistoryBase(BaseModel):
    medical_history: str
    allergies: Optional[str] = None

class PatientHistoryCreate(PatientHistoryBase):
    patient_id: int

class PatientHistoryUpdate(BaseModel):
    medical_history: Optional[str] = None
    allergies: Optional[str] = None

class PatientHistoryResponse(PatientHistoryBase):
    id: int
    patient_id: int

    class Config:
        orm_mode = True


# Billing Schemas
class BillingBase(BaseModel):
    total_amount: float
    paid: bool
    payment_date: Optional[date] = None

class BillingCreate(BillingBase):
    appointment_id: int

class BillingUpdate(BaseModel):
    total_amount: Optional[float] = None
    paid: Optional[bool] = None
    payment_date: Optional[date] = None

class BillingResponse(BillingBase):
    id: int
    appointment_id: int

    class Config:
        orm_mode = True
