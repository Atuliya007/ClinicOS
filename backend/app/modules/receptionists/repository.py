from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.modules.receptionists.models import Receptionist


class ReceptionistRepository(BaseRepository[Receptionist]):
    def __init__(self):
        super().__init__(Receptionist)

    def get_by_phone(self, db: Session, phone: str):
        return db.scalar(select(Receptionist).where(Receptionist.phone_number == phone))

    def get_by_email(self, db: Session, email: str):
        return db.scalar(select(Receptionist).where(Receptionist.email == email))

    def latest(self, db: Session):
        return db.scalar(select(Receptionist).order_by(Receptionist.receptionist_code.desc()).limit(1))

    def filtered(self, db: Session, active=None, shift=None):
        query = select(Receptionist)
        if active is not None: query = query.where(Receptionist.is_active == active)
        if shift is not None: query = query.where(Receptionist.shift == shift)
        return list(db.scalars(query).all())
