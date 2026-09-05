from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.enums.receptionist import Shift
class ReceptionistCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr | None = None
    phone_number: str
    shift: Shift


class ReceptionistUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    shift: Shift | None = None
    is_active: bool | None = None


class ReceptionistResponse(ReceptionistCreate):
    id: UUID
    receptionist_code: str
    is_active: bool

    model_config = {"from_attributes": True}
