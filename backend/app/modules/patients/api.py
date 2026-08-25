from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.dependencies import get_db
from app.modules.patients.schemas import (
    PatientCreate,
    PatientResponse,
)
from app.modules.patients.service import PatientService
from app.modules.patients.schemas import PatientUpdate

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)

service = PatientService()


@router.post(
    "",
    response_model=PatientResponse,
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
):
    return service.create_patient(db, patient)


@router.get(
    "",
    response_model=list[PatientResponse],
)
def get_all_patients(
    db: Session = Depends(get_db),
):
    return service.get_all_patients(db)

@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
)
def get_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
):
    return service.get_patient_by_id(
        db,
        patient_id,
    )


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
)
def update_patient(
    patient_id: UUID,
    patient: PatientUpdate,
    db: Session = Depends(get_db),
):
    return service.update_patient(
        db,
        patient_id,
        patient,
    )



@router.delete(
    "/{patient_id}",
    response_model=PatientResponse,
)
def delete_patient(
    patient_id: UUID,
    db: Session = Depends(get_db),
):
    return service.delete_patient(
        db,
        patient_id,
    )