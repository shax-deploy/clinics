from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List

from app.core.auth import hash_password
from app.database import get_db
from app.models.user import User
from app.models.clinics import Doctor
from app.models.clinics import Patient, DoctorService

from app.schemas.clinics import (
    DoctorCreate, DoctorUpdate, DoctorResponse,
    DoctorServiceCreate, DoctorServiceUpdate, DoctorServiceResponse,
    PatientCreate, PatientUpdate, PatientResponse,
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
    PatientHistoryCreate, PatientHistoryUpdate, PatientHistoryResponse,
    BillingCreate, BillingUpdate, BillingResponse
)
from app.crud.clinics import (
    doctor_crud, doctor_service_crud, patient_crud, 
    appointment_crud, patient_history_crud, billing_crud
)

router = APIRouter()

#-----------------------------------------------------------------------------------------------------

# doctor create
@router.post("/doctors/", response_model=DoctorResponse)
def create_doctor(doctor_data: DoctorCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == doctor_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    if db.query(User).filter(User.phone == doctor_data.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone already registered",
        )
    
    if not doctor_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required",
        )
    
    hashed_password = hash_password(doctor_data.password)
    
    user_data = doctor_data.dict(exclude={"specialization"})  # Faqat kiritilgan qiymatlar
    user_data["password"] = hashed_password
    user_data["role"] = "doctor"

    doctor = doctor_crud.create_with_doctor(
        db=db,
        user_data=user_data,
        doctor_data={"specialization": doctor_data.specialization},
    )
    return doctor

@router.get("/doctors/", response_model=List[DoctorResponse])
def get_doctors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return doctor_crud.get_multi(db=db, skip=skip, limit=limit)

@router.get("/doctors/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_crud.get(db=db, id=doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.patch("/doctors/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db)):
    updated_doctor = doctor_crud.update_patch_with_doctor(db=db, doctor_id=doctor_id, doctor_data=doctor)
    return updated_doctor

@router.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    db_doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(db_doctor.user)

    db.delete(db_doctor)
    db.commit()

    return {"detail": "Doctor and associated user deleted"}

# -------------------------------------------------------------------------------------------------------------


# DoctorService endpoints
@router.post("/services/", response_model=DoctorServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: DoctorServiceCreate, db: Session = Depends(get_db)):
    existing_service = db.query(DoctorService).filter(
        DoctorService.doctor_id == service.doctor_id,
        DoctorService.service_name == service.service_name
    ).first()
    
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with name '{service.service_name}' already exists for this doctor."
        )
    return doctor_service_crud.create(db=db, obj_in=service)

@router.get("/services/", response_model=List[DoctorServiceResponse])
def get_services(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return doctor_service_crud.get_multi(db=db, skip=skip, limit=limit)

@router.get("/service/{service_id}", response_model=DoctorServiceResponse)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = doctor_service_crud.get(db=db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.patch("/service/{service_id}", response_model=DoctorServiceResponse)
def update_service(service_id: int, service: DoctorServiceUpdate, db: Session = Depends(get_db)):
    db_service = doctor_service_crud.get(db=db, id=service_id)
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    existing_service = db.query(DoctorService).filter(
        DoctorService.doctor_id == service.doctor_id,
        DoctorService.service_name == service.service_name
    ).first()
    
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with name '{service.service_name}' already exists for this doctor.")
    return doctor_service_crud.update(db=db, db_obj=db_service, obj_in=service)

@router.delete("/service/{service_id}", response_model=DoctorServiceResponse)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = doctor_service_crud.get(db=db, id=service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return doctor_service_crud.delete(db=db, id=service_id)

# -------------------------------------------------------------------------------------------------------------

# Patient endpoints
@router.post("/patients/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):

    required_fields = ["first_name", "phone"]
    
    for field in required_fields:
        if not getattr(patient, field):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field.replace('_', ' ').capitalize()} is required",
            )
    
    if db.query(Patient).filter(Patient.phone == patient.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone already registered",
        )
    
    
    patient_data = {
        "first_name": patient.first_name,
        "phone": patient.phone,
    }

    if patient.email:
        patient_data["email"] = patient.email

    if patient.last_name:
        patient_data["last_name"] = patient.last_name

    if patient.date_of_birth:
        patient_data["date_of_birth"] = patient.date_of_birth
    return patient_crud.create_patient(db=db, obj_in=patient_data)


@router.get("/patients/", response_model=List[PatientResponse])
def get_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return patient_crud.get_multi(db=db, skip=skip, limit=limit)

@router.get("/patient/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = patient_crud.get(db=db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.patch("/patients/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    db_patient = patient_crud.get(db=db, id=patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_crud.update(db=db, db_obj=db_patient, obj_in=patient)

@router.delete("/patient/{patient_id}", response_model=PatientResponse)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    service = patient_crud.get(db=db, id=patient_id)
    if not service:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_crud.remove(db=db, id=patient_id)

# @router.patch("/patient/{patient_id}", response_model=PatientResponse)
# def update_patient(patient_id: int, patient: PatientUpdate, request: Request, db: Session = Depends(get_db)):
#     db_patient = patient_crud.get(db=db, id=patient_id)
#     if not db_patient:
#         raise HTTPException(status_code=404, detail="Patient not found")
    
#     if request.method == "PUT":
#         updated_data = patient.dict()
#         for key, value in updated_data.items():
#             setattr(db_patient, key, value)
#     elif request.method == "PATCH":
#         updated_data = patient.dict(exclude_unset=True)
#         for key, value in updated_data.items():
#             setattr(db_patient, key, value)

#     db.commit()
#     db.refresh(db_patient)
#     return db_patient

# ------------------------------------------------------------------------------------------------------------

@router.post("/appointments/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    return appointment_crud.create(db=db, obj_in=appointment)

@router.get("/appointments/", response_model=List[AppointmentResponse])
def get_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return appointment_crud.get_multi(db=db, skip=skip, limit=limit)

# ----------------------------------------------------------------------------------------------------------

# PatientHistory endpoints
@router.post("/histories/", response_model=PatientHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_patient_history(history: PatientHistoryCreate, db: Session = Depends(get_db)):
    return patient_history_crud.create(db=db, obj_in=history)

@router.get("/histories/", response_model=List[PatientHistoryResponse])
def get_patient_histories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return patient_history_crud.get_multi(db=db, skip=skip, limit=limit)

# ------------------------------------------------------------------------------------------------------------
# Billing endpoints
@router.post("/billings/", response_model=BillingResponse, status_code=status.HTTP_201_CREATED)
def create_billing(billing: BillingCreate, db: Session = Depends(get_db)):
    return billing_crud.create(db=db, obj_in=billing)

@router.get("/billings/", response_model=List[BillingResponse])
def get_billings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return billing_crud.get_multi(db=db, skip=skip, limit=limit)
