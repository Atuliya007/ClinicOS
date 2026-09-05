from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.enums.billing import PaymentStatus
from app.modules.billing.models import Invoice,InvoiceItem,Payment
from app.modules.billing.schemas import InvoiceCreate,InvoiceResponse,PaymentCreate
from app.modules.patients.models import Patient
router=APIRouter(prefix="/billing",tags=["Billing"])
@router.post("/invoices",response_model=InvoiceResponse,status_code=status.HTTP_201_CREATED)
def create_invoice(data:InvoiceCreate,db:Session=Depends(get_db)):
 if not db.get(Patient,data.patient_id):raise HTTPException(404,"Patient not found")
 latest=db.scalar(select(Invoice).order_by(Invoice.invoice_code.desc()).limit(1));total=sum((x.quantity*x.unit_price for x in data.items),Decimal("0"))
 item=Invoice(invoice_code=f"IV{(int(latest.invoice_code[2:])+1)if latest else 1:06d}",patient_id=data.patient_id,appointment_id=data.appointment_id,total_amount=total);db.add(item);db.flush()
 for x in data.items:db.add(InvoiceItem(invoice_id=item.id,description=x.description,quantity=x.quantity,unit_price=x.unit_price,line_total=x.quantity*x.unit_price))
 db.commit();db.refresh(item);return item
@router.get("/invoices/{item_id}",response_model=InvoiceResponse)
def get_invoice(item_id:UUID,db:Session=Depends(get_db)):
 item=db.get(Invoice,item_id)
 if not item:raise HTTPException(404,"Invoice not found")
 return item
@router.post("/invoices/{item_id}/payments",response_model=InvoiceResponse)
def pay(item_id:UUID,data:PaymentCreate,db:Session=Depends(get_db)):
 item=db.get(Invoice,item_id)
 if not item:raise HTTPException(404,"Invoice not found")
 if item.payment_status==PaymentStatus.CANCELLED:raise HTTPException(400,"Invoice is cancelled")
 if item.paid_amount+data.amount>item.total_amount:raise HTTPException(400,"Payment exceeds invoice balance")
 db.add(Payment(invoice_id=item.id,**data.model_dump()));item.paid_amount+=data.amount;item.payment_status=PaymentStatus.PAID if item.paid_amount==item.total_amount else PaymentStatus.PARTIALLY_PAID;db.commit();db.refresh(item);return item
