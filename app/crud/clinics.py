from sqlalchemy.orm import Session
from app.models.clinics import Doctor, DoctorService, Patient, Appointment, PatientHistory, Billing
from app.schemas.clinics import (
    DoctorCreate, DoctorUpdate, 
    DoctorServiceCreate, DoctorServiceUpdate, 
    PatientCreate, PatientUpdate, 
    AppointmentCreate, AppointmentUpdate, 
    PatientHistoryCreate, PatientHistoryUpdate, 
    BillingCreate, BillingUpdate
)
from app.crud.base import CRUDBase
from app.crud.base import CRUDDoctor


doctor_crud = CRUDDoctor(Doctor)

# DoctorService uchun CRUD
class CRUDDoctorService(CRUDBase[DoctorService, DoctorServiceCreate, DoctorServiceUpdate]):
    def get_services_by_doctor(self, db: Session, doctor_id: int):
        return db.query(DoctorService).filter(DoctorService.doctor_id == doctor_id).all()


# Patient uchun CRUD
class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    def get_patient_by_patient(self, db: Session, patient_id: str):
        return db.query(Patient).filter(Patient.id == patient_id).first()


# Appointment uchun CRUD
class CRUDApartment(CRUDBase[Appointment, AppointmentCreate, AppointmentUpdate]):
    def get_appointments_by_doctor(self, db: Session, doctor_id: int):
        return db.query(Appointment).filter(Appointment.doctor_id == doctor_id).all()

    def get_appointments_by_patient(self, db: Session, patient_id: int):
        return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


# PatientHistory uchun CRUD
class CRUDPatientHistory(CRUDBase[PatientHistory, PatientHistoryCreate, PatientHistoryUpdate]):
    def get_history_by_patient(self, db: Session, patient_id: int):
        return db.query(PatientHistory).filter(PatientHistory.patient_id == patient_id).first()


# Billing uchun CRUD
class CRUDBilling(CRUDBase[Billing, BillingCreate, BillingUpdate]):
    def get_billing_by_appointment(self, db: Session, appointment_id: int):
        return db.query(Billing).filter(Billing.appointment_id == appointment_id).first()


doctor_service_crud = CRUDDoctorService(DoctorService)
patient_crud = CRUDPatient(Patient)
appointment_crud = CRUDApartment(Appointment)
patient_history_crud = CRUDPatientHistory(PatientHistory)
billing_crud = CRUDBilling(Billing)
