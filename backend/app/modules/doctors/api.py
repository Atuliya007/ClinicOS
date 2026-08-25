from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.modules.doctors.schemas import (
    DoctorCreate,
    DoctorResponse,
    DoctorUpdate,
)
from app.modules.doctors.service import DoctorService


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)

service = DoctorService()


@router.post(
    "",
    response_model=DoctorResponse,
)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
):
    return service.create_doctor(
        db,
        doctor,
    )


@router.get(
    "",
    response_model=list[DoctorResponse],
)
def get_all_doctors(
    db: Session = Depends(get_db),
):
    return service.get_all_doctors(db)


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
def get_doctor(
    doctor_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_doctor_by_id(
        db,
        doctor_id,
    )


@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse,
)
def update_doctor(
    doctor_id: UUID,
    doctor: DoctorUpdate,
    db: Session = Depends(get_db),
):
    return service.update_doctor(
        db,
        doctor_id,
        doctor,
    )