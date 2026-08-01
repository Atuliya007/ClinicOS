from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.modules.patients.models import Patient


class PatientRepository:

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
            .order_by(desc(Patient.patient_code))
            .limit(1)
        )

        return db.scalar(statement)

    def create(
        self,
        db: Session,
        patient: Patient,
    ) -> Patient:

        db.add(patient)
        db.commit()
        db.refresh(patient)

        return patient

    def get_all(
    self,
    db: Session,
    ) -> list[Patient]:

     statement = select(Patient).order_by(
        Patient.created_at.desc()
    )

     return list(db.scalars(statement).all())