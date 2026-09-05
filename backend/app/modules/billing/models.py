from decimal import Decimal
from uuid import UUID
from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.enums.billing import PaymentMethod, PaymentStatus
from app.models.base_model import BaseModel
class Invoice(BaseModel):
    __tablename__="invoices"
    invoice_code:Mapped[str]=mapped_column(String(20),unique=True)
    patient_id:Mapped[UUID]=mapped_column(ForeignKey("patients.id"),index=True)
    appointment_id:Mapped[UUID|None]=mapped_column(ForeignKey("appointments.id"),nullable=True)
    total_amount:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0)
    paid_amount:Mapped[Decimal]=mapped_column(Numeric(12,2),default=0)
    payment_status:Mapped[PaymentStatus]=mapped_column(Enum(PaymentStatus),default=PaymentStatus.PENDING)
class InvoiceItem(BaseModel):
    __tablename__="invoice_items"
    invoice_id:Mapped[UUID]=mapped_column(ForeignKey("invoices.id"),index=True)
    description:Mapped[str]=mapped_column(String(255))
    quantity:Mapped[int]=mapped_column(default=1)
    unit_price:Mapped[Decimal]=mapped_column(Numeric(12,2))
    line_total:Mapped[Decimal]=mapped_column(Numeric(12,2))
class Payment(BaseModel):
    __tablename__="payments"
    invoice_id:Mapped[UUID]=mapped_column(ForeignKey("invoices.id"),index=True)
    amount:Mapped[Decimal]=mapped_column(Numeric(12,2))
    method:Mapped[PaymentMethod]=mapped_column(Enum(PaymentMethod))
