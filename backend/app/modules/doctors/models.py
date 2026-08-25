from sqlalchemy import Boolean, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.doctor import Specialization
from app.models.base_model import BaseModel


class Doctor(BaseModel):
    __tablename__ = "doctors"

    doctor_code: Mapped[str] = mapped_column(
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

    specialization: Mapped[Specialization] = mapped_column(
        Enum(Specialization),
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

    qualification: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    consultation_fee: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )