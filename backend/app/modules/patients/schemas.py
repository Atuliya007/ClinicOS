from datetime import date
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.patient import BloodGroup, Gender


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    phone_number: str
    email: EmailStr | None = None
    blood_group: BloodGroup | None = None

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )


class PatientResponse(BaseModel):
    id: UUID
    patient_code: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    phone_number: str
    email: EmailStr | None
    blood_group: BloodGroup | None
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class PatientUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    blood_group: BloodGroup | None = None
    is_active: bool | None = None

