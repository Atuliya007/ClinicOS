from uuid import UUID
from pydantic import BaseModel
class DepartmentCreate(BaseModel): name: str; description: str | None = None
class DepartmentUpdate(BaseModel): name: str | None = None; description: str | None = None; is_active: bool | None = None
class DepartmentResponse(DepartmentCreate):
    id: UUID; department_code: str; is_active: bool
    model_config = {"from_attributes": True}
