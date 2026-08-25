from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.enums.doctor import Specialization


class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialization: Specialization
    phone_number: str
    email: EmailStr | None = None
    qualification: str
    years_of_experience: int
    consultation_fee: float

class DoctorUpdate(BaseModel):
    first_name: str
    last_name: str
    specialization: Specialization
    phone_number: str
    email: EmailStr | None = None
    qualification: str
    years_of_experience: int
    consultation_fee: float
    

class DoctorResponse(DoctorCreate):
    id: UUID
    doctor_code: str

    model_config = {
        "from_attributes": True,
    }