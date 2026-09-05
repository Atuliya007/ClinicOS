from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.modules.doctors.models import Doctor


class DoctorRepository(BaseRepository[Doctor]):

    def __init__(self):
        super().__init__(Doctor)

    def get_latest_doctor(
        self,
        db: Session,
    ) -> Doctor | None:

        statement = (
            select(Doctor)
            .order_by(Doctor.doctor_code.desc())
            .limit(1)
        )

        return db.scalar(statement)

    def get_by_phone(self, db: Session, phone_number: str) -> Doctor | None:
        return db.scalar(select(Doctor).where(Doctor.phone_number == phone_number))

    def get_all_filtered(self, db: Session, active: bool | None = None, specialization=None) -> list[Doctor]:
        statement = select(Doctor)
        if active is not None:
            statement = statement.where(Doctor.is_active == active)
        if specialization is not None:
            statement = statement.where(Doctor.specialization == specialization)
        return list(db.scalars(statement).all())
