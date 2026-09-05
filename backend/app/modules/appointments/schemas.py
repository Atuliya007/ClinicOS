"""Schemas and UTC normalization for appointment scheduling.

ClinicOS treats a datetime without an offset as UTC. Offset-aware values are
converted to UTC, so all application comparisons and persisted values use one
unambiguous timeline.
"""

from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.enums.appointment import AppointmentStatus


def normalize_appointment_datetime(value: datetime) -> datetime:
    """Return an offset-aware UTC datetime, treating naive input as UTC."""
    if value.tzinfo is None or value.utcoffset() is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


class AppointmentDatetimeSchema(BaseModel):
    appointment_datetime: datetime

    @field_validator("appointment_datetime")
    @classmethod
    def normalize_datetime(cls, value: datetime) -> datetime:
        return normalize_appointment_datetime(value)


class AppointmentCreate(AppointmentDatetimeSchema):
    patient_id: UUID
    doctor_id: UUID
    receptionist_id: UUID
    problem: str = Field(min_length=1)
    notes: str | None = None


class AppointmentStatusUpdate(BaseModel):
    appointment_status: AppointmentStatus


class AppointmentUpdate(BaseModel):
    notes: str | None = None


class RescheduleAppointment(AppointmentDatetimeSchema):
    pass


class AppointmentResponse(AppointmentCreate):
    id: UUID
    appointment_status: AppointmentStatus

    model_config = {"from_attributes": True}
