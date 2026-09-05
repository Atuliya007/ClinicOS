from uuid import UUID
from app.modules.receptionists.exceptions import ReceptionistConflictException, ReceptionistNotFoundException
from app.modules.receptionists.models import Receptionist
from app.modules.receptionists.repository import ReceptionistRepository
from app.modules.receptionists.schemas import ReceptionistCreate, ReceptionistUpdate


class ReceptionistService:
    def __init__(self): self.repository = ReceptionistRepository()
    def get(self, db, item_id: UUID):
        item = self.repository.get_by_id(db, item_id)
        if not item: raise ReceptionistNotFoundException()
        return item
    def create(self, db, data: ReceptionistCreate):
        if self.repository.get_by_phone(db, data.phone_number) or (data.email and self.repository.get_by_email(db, str(data.email))):
            raise ReceptionistConflictException()
        latest = self.repository.latest(db)
        code = f"RC{(int(latest.receptionist_code[2:]) + 1) if latest else 1:06d}"
        return self.repository.create(db, Receptionist(receptionist_code=code, **data.model_dump()))
    def update(self, db, item_id, data: ReceptionistUpdate):
        item = self.get(db, item_id)
        for key, value in data.model_dump(exclude_unset=True).items(): setattr(item, key, value)
        return self.repository.update(db, item)
