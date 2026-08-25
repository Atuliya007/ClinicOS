from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.base_repository import BaseRepository
from app.modules.patients.models import Patient


class PatientRepository(BaseRepository[Patient]):

    def __init__(self):
        super().__init__(Patient)

    def get_by_phone(
        self,
        db: Session,
        phone_number: str,
    ) -> Patient | None:

        statement = select(Patient).where(
            Patient.phone_number == phone_number
        )

        return db.scalar(statement)

    def get_latest_patient(
        self,
        db: Session,
    ) -> Patient | None:

        statement = (
            select(Patient)
            .order_by(Patient.patient_code.desc())
            .limit(1)
        )

        return db.scalar(statement)