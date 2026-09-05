from datetime import datetime
from uuid import UUID
from sqlalchemy import DateTime, Enum, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.enums.appointment import AppointmentStatus
from app.models.base_model import BaseModel
class Appointment(BaseModel):
    __tablename__ = "appointments"
    __table_args__ = (Index("uq_doctor_appointment_datetime", "doctor_id", "appointment_datetime", unique=True),)
    patient_id: Mapped[UUID] = mapped_column(ForeignKey("patients.id"), index=True)
    doctor_id: Mapped[UUID] = mapped_column(ForeignKey("doctors.id"), index=True)
    receptionist_id: Mapped[UUID] = mapped_column(ForeignKey("receptionists.id"), index=True)
    problem: Mapped[str] = mapped_column(Text)
    appointment_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    appointment_status: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.PENDING)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
