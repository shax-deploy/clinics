from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

# Doctor Model
class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specialization = Column(String)

    # Bog'lanishlar
    services = relationship("DoctorService", back_populates="doctor")  # One-to-Many
    appointments = relationship("Appointment", back_populates="doctor")  # One-to-Many


# DoctorService Model
class DoctorService(Base):
    __tablename__ = "doctor_services"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service_name = Column(String, index=True)
    price = Column(Numeric(10, 2))

    # Bog'lanish
    doctor = relationship("Doctor", back_populates="services")  # Many-to-One
    appointments = relationship("Appointment", back_populates="service")  # One-to-Many


# Patient Model
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True)
    email = Column(String, unique=True)
    date_of_birth = Column(DateTime, nullable=True)

    # Bog'lanishlar
    appointments = relationship("Appointment", back_populates="patient")  # One-to-Many
    history = relationship("PatientHistory", back_populates="patient", uselist=False)  # One-to-One


# Appointment Model
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    service_id = Column(Integer, ForeignKey("doctor_services.id"))
    appointment_date = Column(DateTime)
    notes = Column(Text, nullable=True)

    # Bog'lanishlar
    patient = relationship("Patient", back_populates="appointments")  # Many-to-One
    doctor = relationship("Doctor", back_populates="appointments")  # Many-to-One
    service = relationship("DoctorService", back_populates="appointments")  # Many-to-One
    billing = relationship("Billing", back_populates="appointment", uselist=False)  # One-to-One


# PatientHistory Model
class PatientHistory(Base):
    __tablename__ = "patient_histories"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medical_history = Column(Text)
    allergies = Column(Text, nullable=True)

    # Bog'lanish
    patient = relationship("Patient", back_populates="history")  # One-to-One


# Billing Model
class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    total_amount = Column(Numeric(10, 2))
    paid = Column(Boolean, default=False)
    payment_date = Column(DateTime, nullable=True)

    # Bog'lanish
    appointment = relationship("Appointment", back_populates="billing")  # One-to-One
