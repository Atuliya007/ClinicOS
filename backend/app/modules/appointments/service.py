from datetime import datetime, timezone

from fastapi import HTTPException

from app.enums.appointment import AppointmentStatus
from app.modules.appointments.models import Appointment
from app.modules.appointments.repository import AppointmentRepository
from app.modules.appointments.schemas import normalize_appointment_datetime
from app.modules.doctors.models import Doctor
from app.modules.patients.models import Patient
from app.modules.receptionists.models import Receptionist


class AppointmentService:
    transitions = {
        AppointmentStatus.PENDING: {
            AppointmentStatus.WAITING,
            AppointmentStatus.CANCELLED,
            AppointmentStatus.NO_SHOW,
        },
        AppointmentStatus.WAITING: {
            AppointmentStatus.IN_PROCESS,
            AppointmentStatus.CANCELLED,
            AppointmentStatus.NO_SHOW,
        },
        AppointmentStatus.IN_PROCESS: {AppointmentStatus.COMPLETED},
    }

    def __init__(self):
        self.repository = AppointmentRepository()

    @staticmethod
    def validate_future_datetime(value: datetime) -> datetime:
        normalized = normalize_appointment_datetime(value)
        if normalized <= datetime.now(timezone.utc):
            raise HTTPException(400, "Appointment time must be in the future")
        return normalized

    def get(self, db, item_id):
        item = self.repository.get_by_id(db, item_id)
        if not item:
            raise HTTPException(404, "Appointment not found")
        return item

    def create(self, db, data):
        appointment_datetime = self.validate_future_datetime(data.appointment_datetime)
        patient = db.get(Patient, data.patient_id)
        doctor = db.get(Doctor, data.doctor_id)
        receptionist = db.get(Receptionist, data.receptionist_id)
        if not patient:
            raise HTTPException(404, "Patient not found")
        if not doctor:
            raise HTTPException(404, "Doctor not found")
        if not receptionist:
            raise HTTPException(404, "Receptionist not found")
        if not patient.is_active:
            raise HTTPException(400, "Patient is inactive")
        if not doctor.is_active:
            raise HTTPException(400, "Doctor is inactive")
        if not receptionist.is_active:
            raise HTTPException(400, "Receptionist is inactive")
        if self.repository.conflict(db, data.doctor_id, appointment_datetime):
            raise HTTPException(409, "Doctor is already booked at this time")
        values = data.model_dump()
        values["appointment_datetime"] = appointment_datetime
        return self.repository.create(db, Appointment(**values))

    def reschedule(self, db, item_id, appointment_datetime):
        item = self.get(db, item_id)
        if item.appointment_status not in {
            AppointmentStatus.PENDING,
            AppointmentStatus.WAITING,
        }:
            raise HTTPException(400, "Only pending or waiting appointments may be rescheduled")
        normalized = self.validate_future_datetime(appointment_datetime)
        if self.repository.conflict(db, item.doctor_id, normalized, item.id):
            raise HTTPException(409, "Doctor is already booked at this time")
        item.appointment_datetime = normalized
        return self.repository.update(db, item)

    def status(self, db, item_id, new_status):
        item = self.get(db, item_id)
        if new_status not in self.transitions.get(item.appointment_status, set()):
            raise HTTPException(400, "Invalid appointment status transition")
        item.appointment_status = new_status
        return self.repository.update(db, item)
