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