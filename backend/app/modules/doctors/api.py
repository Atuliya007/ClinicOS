from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.modules.doctors.schemas import (
    DoctorCreate,
    DoctorResponse,
    DoctorUpdate,
)
from app.modules.doctors.service import DoctorService
from app.enums.doctor import Specialization


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)

service = DoctorService()


@router.post(
    "",
    response_model=DoctorResponse,
    status_code=status.HTTP_201_CREATED,
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
    active: bool | None = Query(default=None),
    specialization: Specialization | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return service.get_all_doctors(db, active, specialization)


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


@router.patch(
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
