from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel,Field
from app.enums.billing import PaymentMethod,PaymentStatus
class InvoiceItemCreate(BaseModel):description:str;quantity:int=Field(gt=0);unit_price:Decimal=Field(ge=0)
class InvoiceCreate(BaseModel):patient_id:UUID;appointment_id:UUID|None=None;items:list[InvoiceItemCreate]=Field(min_length=1)
class InvoiceResponse(BaseModel):id:UUID;invoice_code:str;patient_id:UUID;total_amount:Decimal;paid_amount:Decimal;payment_status:PaymentStatus;model_config={"from_attributes":True}
class PaymentCreate(BaseModel):amount:Decimal=Field(gt=0);method:PaymentMethod
