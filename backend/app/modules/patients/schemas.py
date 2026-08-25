from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.patient import BloodGroup, Gender


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    phone_number: str
    email: Optional[EmailStr] = None
    blood_group: Optional[BloodGroup] = None

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
    email: Optional[EmailStr]
    blood_group: Optional[BloodGroup]
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class PatientUpdate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    phone_number: str
    email: EmailStr | None = None
    blood_group: BloodGroup | None = None

