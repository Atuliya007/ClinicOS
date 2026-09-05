from datetime import date
from sqlalchemy import Boolean, Date, Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.patient import BloodGroup, Gender
from app.models.base_model import BaseModel

class Patient(BaseModel):
    __tablename__ = "patients"
    __table_args__ = (Index("ix_patients_phone_number", "phone_number", unique=True),)

    patient_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        Enum(Gender),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    blood_group: Mapped[BloodGroup | None] = mapped_column(
        Enum(BloodGroup),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
