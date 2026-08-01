from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.modules.patients.schemas import (
    PatientCreate,
    PatientResponse,
)
from app.modules.patients.service import PatientService

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