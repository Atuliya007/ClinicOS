from datetime import date
from uuid import UUID
from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.enums.appointment import AppointmentStatus
from app.modules.appointments.schemas import AppointmentCreate,AppointmentResponse,AppointmentStatusUpdate,AppointmentUpdate,RescheduleAppointment
from app.modules.appointments.service import AppointmentService
router=APIRouter(prefix="/appointments",tags=["Appointments"]); service=AppointmentService()
@router.post("",response_model=AppointmentResponse,status_code=status.HTTP_201_CREATED)
def create(data:AppointmentCreate,db:Session=Depends(get_db)): return service.create(db,data)
@router.get("",response_model=list[AppointmentResponse])
def list_items(patient_id:UUID|None=None,doctor_id:UUID|None=None,receptionist_id:UUID|None=None,on_date:date|None=None,db:Session=Depends(get_db)): return service.repository.filtered(db,patient_id,doctor_id,receptionist_id,on_date)
@router.get("/{item_id}",response_model=AppointmentResponse)
def get(item_id:UUID,db:Session=Depends(get_db)): return service.get(db,item_id)
@router.post("/{item_id}/status",response_model=AppointmentResponse)
def update_status(item_id:UUID,data:AppointmentStatusUpdate,db:Session=Depends(get_db)): return service.status(db,item_id,data.appointment_status)
@router.post("/{item_id}/cancel",response_model=AppointmentResponse)
def cancel(item_id:UUID,db:Session=Depends(get_db)): return service.status(db,item_id,AppointmentStatus.CANCELLED)
@router.post("/{item_id}/reschedule",response_model=AppointmentResponse)
def reschedule(item_id:UUID,data:RescheduleAppointment,db:Session=Depends(get_db)):
    return service.reschedule(db, item_id, data.appointment_datetime)
