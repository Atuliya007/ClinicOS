from uuid import UUID

from app.modules.doctors.exceptions import DoctorConflictException, DoctorNotFoundException
from app.modules.doctors.models import Doctor
from app.modules.doctors.repository import DoctorRepository
from app.modules.doctors.schemas import DoctorCreate, DoctorUpdate


class DoctorService:
    def __init__(self):
        self.repository = DoctorRepository()

    def create_doctor(self, db, data: DoctorCreate) -> Doctor:
        if self.repository.get_by_phone(db, data.phone_number):
            raise DoctorConflictException()
        latest = self.repository.get_latest_doctor(db)
        code = f"DR{(int(latest.doctor_code[2:]) + 1) if latest else 1:06d}"
        return self.repository.create(db, Doctor(doctor_code=code, **data.model_dump()))

    def get_all_doctors(self, db, active=None, specialization=None) -> list[Doctor]:
        return self.repository.get_all_filtered(db, active, specialization)

    def get_doctor_by_id(self, db, doctor_id: UUID) -> Doctor:
        doctor = self.repository.get_by_id(db, doctor_id)
        if doctor is None:
            raise DoctorNotFoundException()
        return doctor

    def update_doctor(self, db, doctor_id: UUID, data: DoctorUpdate) -> Doctor:
        doctor = self.get_doctor_by_id(db, doctor_id)
        values = data.model_dump(exclude_unset=True)
        phone = values.get("phone_number")
        if phone and phone != doctor.phone_number:
            existing = self.repository.get_by_phone(db, phone)
            if existing and existing.id != doctor.id:
                raise DoctorConflictException()
        for field, value in values.items():
            setattr(doctor, field, value)
        return self.repository.update(db, doctor)
