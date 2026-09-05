from uuid import UUID

from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field

from app.enums.doctor import Specialization


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: Specialization
    phone_number: str
    email: EmailStr | None = None
    qualification: str
    years_of_experience: int
    consultation_fee: Decimal = Field(ge=0)

class DoctorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    specialization: Specialization | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    qualification: str | None = None
    years_of_experience: int | None = Field(default=None, ge=0)
    consultation_fee: Decimal | None = Field(default=None, ge=0)
    is_active: bool | None = None
    

class DoctorResponse(DoctorCreate):
    id: UUID
    doctor_code: str
    is_active: bool

    model_config = {
        "from_attributes": True,
    }
