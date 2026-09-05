from datetime import datetime,timezone
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.enums.laboratory import LabOrderStatus
from app.modules.laboratory.models import LabOrder,LabTest
from app.modules.laboratory.schemas import LabOrderCreate,LabOrderResponse,LabOrderUpdate,LabTestCreate,LabTestResponse
from app.modules.patients.models import Patient
router=APIRouter(prefix="/laboratory",tags=["Laboratory"])
@router.post("/tests",response_model=LabTestResponse,status_code=status.HTTP_201_CREATED)
def create_test(data:LabTestCreate,db:Session=Depends(get_db)):
    latest=db.scalar(select(LabTest).order_by(LabTest.test_code.desc()).limit(1)); item=LabTest(test_code=f"LT{(int(latest.test_code[2:])+1) if latest else 1:06d}",**data.model_dump());db.add(item);db.commit();db.refresh(item);return item
@router.get("/tests",response_model=list[LabTestResponse])
def list_tests(db:Session=Depends(get_db)):return list(db.scalars(select(LabTest)).all())
@router.post("/orders",response_model=LabOrderResponse,status_code=status.HTTP_201_CREATED)
def create_order(data:LabOrderCreate,db:Session=Depends(get_db)):
    if not db.get(Patient,data.patient_id):raise HTTPException(404,"Patient not found")
    if not db.get(LabTest,data.lab_test_id):raise HTTPException(404,"Lab test not found")
    item=LabOrder(**data.model_dump());db.add(item);db.commit();db.refresh(item);return item
@router.patch("/orders/{item_id}",response_model=LabOrderResponse)
def update_order(item_id:UUID,data:LabOrderUpdate,db:Session=Depends(get_db)):
    item=db.get(LabOrder,item_id)
    if not item:raise HTTPException(404,"Lab order not found")
    values=data.model_dump(exclude_unset=True)
    if values.get("status")==LabOrderStatus.COMPLETED and not values.get("result") and not item.result:raise HTTPException(400,"Completed order requires a result")
    for k,v in values.items():setattr(item,k,v)
    if item.status==LabOrderStatus.COMPLETED:item.completed_at=datetime.now(timezone.utc)
    db.commit();db.refresh(item);return item
