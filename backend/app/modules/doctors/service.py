from uuid import UUID

from app.modules.doctors.exceptions import (
    DoctorNotFoundException,
)
from app.modules.doctors.models import Doctor
from app.modules.doctors.repository import DoctorRepository
from app.modules.doctors.schemas import (
    DoctorCreate,
    DoctorUpdate,
)


class DoctorService:

    def __init__(self):
        self.repository = DoctorRepository()

    def _generate_doctor_code(
        self,
        latest_doctor: Doctor | None,
    ) -> str:

        if latest_doctor is None:
            return "DR000001"

        number = (
            int(
                latest_doctor.doctor_code.replace(
                    "DR",
                    "",
                )
            )
            + 1
        )

        return f"DR{number:06d}"

    def create_doctor(
        self,
        db,
        doctor_data: DoctorCreate,
    ) -> Doctor:

        latest_doctor = (
            self.repository.get_latest_doctor(db)
        )

        doctor_code = (
            self._generate_doctor_code(
                latest_doctor
            )
        )

        doctor = Doctor(
            doctor_code=doctor_code,
            first_name=doctor_data.first_name,
            last_name=doctor_data.last_name,
            specialization=doctor_data.specialization,
            phone_number=doctor_data.phone_number,
            email=doctor_data.email,
            qualification=doctor_data.qualification,
            years_of_experience=doctor_data.years_of_experience,
            consultation_fee=doctor_data.consultation_fee,
        )

        return self.repository.create(
            db,
            doctor,
        )

    def get_all_doctors(
        self,
        db,
    ) -> list[Doctor]:

        return self.repository.get_all(db)

    def get_doctor_by_id(
        self,
        db,
        doctor_id: UUID,
    ) -> Doctor:

        doctor = self.repository.get_by_id(
            db,
            doctor_id,
        )

        if doctor is None:
            raise DoctorNotFoundException()

        return doctor

    def update_doctor(
        self,
        db,
        doctor_id: UUID,
        doctor_data: DoctorUpdate,
    ) -> Doctor:

        doctor = self.repository.get_by_id(
            db,
            doctor_id,
        )

        if doctor is None:
            raise DoctorNotFoundException()

        doctor.first_name = (
            doctor_data.first_name
        )
        doctor.last_name = (
            doctor_data.last_name
        )
        doctor.specialization = (
            doctor_data.specialization
        )
        doctor.phone_number = (
            doctor_data.phone_number
        )
        doctor.email = doctor_data.email
        doctor.qualification = (
            doctor_data.qualification
        )
        doctor.years_of_experience = (
            doctor_data.years_of_experience
        )
        doctor.consultation_fee = (
            doctor_data.consultation_fee
        )

        return self.repository.update(
            db,
            doctor,
        )