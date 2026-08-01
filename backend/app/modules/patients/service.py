from app.modules.patients.models import Patient
from app.modules.patients.repository import PatientRepository
from app.modules.patients.schemas import PatientCreate


class PatientService:

    
    def __init__(self):
        self.repository = PatientRepository()

    def _generate_patient_code(
        self,
        latest_patient: Patient | None,
    ) -> str:

        if latest_patient is None:
            return "PAT000001"

        number = int(latest_patient.patient_code.replace("PAT", "")) + 1

        return f"PAT{number:06d}"

    def create_patient(
        self,
        db,
        patient_data: PatientCreate,
    ) -> Patient:

        existing_patient = self.repository.get_by_phone(
            db,
            patient_data.phone_number,
        )

        if existing_patient:
            return existing_patient

        latest_patient = self.repository.get_latest_patient(db)

        patient_code = self._generate_patient_code(
            latest_patient
        )

        patient = Patient(
            patient_code=patient_code,
            first_name=patient_data.first_name,
            last_name=patient_data.last_name,
            date_of_birth=patient_data.date_of_birth,
            gender=patient_data.gender,
            phone_number=patient_data.phone_number,
            email=patient_data.email,
            blood_group=patient_data.blood_group,
        )

        return self.repository.create(
            db,
            patient,
        )

    def get_all_patients(
    self,
    db,
    ) -> list[Patient]:

        return self.repository.get_all(db)