from uuid import UUID

from app.modules.patients.exceptions import PatientConflictException, PatientNotFoundException
from app.modules.patients.models import Patient
from app.modules.patients.repository import PatientRepository
from app.modules.patients.schemas import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self):
        self.repository = PatientRepository()

    def _generate_patient_code(self, latest: Patient | None) -> str:
        return f"PT{(int(latest.patient_code[-6:]) + 1) if latest else 1:06d}"

    def create_patient(self, db, data: PatientCreate) -> Patient:
        if self.repository.get_by_phone(db, data.phone_number):
            raise PatientConflictException()
        latest = self.repository.get_latest_patient(db)
        patient = Patient(patient_code=self._generate_patient_code(latest), **data.model_dump())
        return self.repository.create(db, patient)

    def get_all_patients(self, db) -> list[Patient]:
        return self.repository.get_all(db)

    def get_patient_by_id(self, db, patient_id: UUID) -> Patient:
        patient = self.repository.get_by_id(db, patient_id)
        if patient is None:
            raise PatientNotFoundException()
        return patient

    def update_patient(self, db, patient_id: UUID, data: PatientUpdate) -> Patient:
        patient = self.get_patient_by_id(db, patient_id)
        values = data.model_dump(exclude_unset=True)
        phone = values.get("phone_number")
        if phone and phone != patient.phone_number:
            existing = self.repository.get_by_phone(db, phone)
            if existing and existing.id != patient.id:
                raise PatientConflictException()
        for field, value in values.items():
            setattr(patient, field, value)
        return self.repository.update(db, patient)

    def delete_patient(self, db, patient_id: UUID) -> Patient:
        patient = self.get_patient_by_id(db, patient_id)
        patient.is_active = False
        return self.repository.update(db, patient)
