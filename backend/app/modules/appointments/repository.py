from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.base_repository import BaseRepository
from app.modules.appointments.models import Appointment
class AppointmentRepository(BaseRepository[Appointment]):
    def __init__(self): super().__init__(Appointment)
    def conflict(self, db: Session, doctor_id, when, exclude_id=None):
        q=select(Appointment).where(Appointment.doctor_id==doctor_id, Appointment.appointment_datetime==when)
        if exclude_id: q=q.where(Appointment.id != exclude_id)
        return db.scalar(q)
    def filtered(self, db: Session, patient_id=None, doctor_id=None, receptionist_id=None, on_date: date | None=None):
        q=select(Appointment)
        if patient_id: q=q.where(Appointment.patient_id==patient_id)
        if doctor_id: q=q.where(Appointment.doctor_id==doctor_id)
        if receptionist_id: q=q.where(Appointment.receptionist_id==receptionist_id)
        if on_date: q=q.where(Appointment.appointment_datetime >= on_date, Appointment.appointment_datetime < date.fromordinal(on_date.toordinal()+1))
        return list(db.scalars(q.order_by(Appointment.appointment_datetime)).all())
