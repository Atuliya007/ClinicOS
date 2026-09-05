from decimal import Decimal
from uuid import UUID
from sqlalchemy import ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base_model import BaseModel
class Medicine(BaseModel):
    __tablename__="medicines"
    medicine_code:Mapped[str]=mapped_column(String(20),unique=True)
    name:Mapped[str]=mapped_column(String(150),unique=True)
    description:Mapped[str|None]=mapped_column(Text,nullable=True)
    unit_price:Mapped[Decimal]=mapped_column(Numeric(10,2))
    stock_quantity:Mapped[int]=mapped_column(Integer,default=0)
    reorder_level:Mapped[int]=mapped_column(Integer,default=0)
    is_active:Mapped[bool]=mapped_column(default=True)
class Prescription(BaseModel):
    __tablename__="prescriptions"
    patient_id:Mapped[UUID]=mapped_column(ForeignKey("patients.id"),index=True)
    doctor_id:Mapped[UUID]=mapped_column(ForeignKey("doctors.id"))
    appointment_id:Mapped[UUID|None]=mapped_column(ForeignKey("appointments.id"),nullable=True)
    notes:Mapped[str|None]=mapped_column(Text,nullable=True)
class PrescriptionItem(BaseModel):
    __tablename__="prescription_items"
    prescription_id:Mapped[UUID]=mapped_column(ForeignKey("prescriptions.id"),index=True)
    medicine_id:Mapped[UUID]=mapped_column(ForeignKey("medicines.id"))
    quantity:Mapped[int]=mapped_column(Integer)
    dosage:Mapped[str]=mapped_column(String(255))
    dispensed_quantity:Mapped[int]=mapped_column(Integer,default=0)
