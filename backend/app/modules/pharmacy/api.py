from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.modules.pharmacy.models import Medicine,Prescription,PrescriptionItem
from app.modules.pharmacy.schemas import MedicineCreate,MedicineResponse,PrescriptionCreate,PrescriptionResponse
from app.modules.patients.models import Patient
from app.modules.doctors.models import Doctor
router=APIRouter(prefix="/pharmacy",tags=["Pharmacy"])
@router.post("/medicines",response_model=MedicineResponse,status_code=status.HTTP_201_CREATED)
def create_medicine(data:MedicineCreate,db:Session=Depends(get_db)):
 latest=db.scalar(select(Medicine).order_by(Medicine.medicine_code.desc()).limit(1));item=Medicine(medicine_code=f"MD{(int(latest.medicine_code[2:])+1)if latest else 1:06d}",**data.model_dump());db.add(item);db.commit();db.refresh(item);return item
@router.get("/medicines",response_model=list[MedicineResponse])
def list_medicines(db:Session=Depends(get_db)):return list(db.scalars(select(Medicine)).all())
@router.post("/prescriptions",response_model=PrescriptionResponse,status_code=status.HTTP_201_CREATED)
def create_prescription(data:PrescriptionCreate,db:Session=Depends(get_db)):
 if not db.get(Patient,data.patient_id) or not db.get(Doctor,data.doctor_id):raise HTTPException(404,"Patient or doctor not found")
 prescription=Prescription(**data.model_dump(exclude={"items"}));db.add(prescription);db.flush()
 for line in data.items:
  medicine=db.get(Medicine,line.medicine_id)
  if not medicine:db.rollback();raise HTTPException(404,"Medicine not found")
  if medicine.stock_quantity<line.quantity:db.rollback();raise HTTPException(409,"Insufficient stock")
  medicine.stock_quantity-=line.quantity;db.add(PrescriptionItem(prescription_id=prescription.id,**line.model_dump(),dispensed_quantity=line.quantity))
 db.commit();db.refresh(prescription);return prescription
