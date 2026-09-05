from datetime import datetime
from decimal import Decimal
from uuid import UUID
from sqlalchemy import Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.enums.laboratory import LabOrderStatus
from app.models.base_model import BaseModel
class LabTest(BaseModel):
    __tablename__="lab_tests"
    test_code: Mapped[str]=mapped_column(String(20),unique=True)
    name: Mapped[str]=mapped_column(String(150),unique=True)
    price: Mapped[Decimal]=mapped_column(Numeric(10,2))
    description: Mapped[str|None]=mapped_column(Text,nullable=True)
    is_active: Mapped[bool]=mapped_column(default=True)
class LabOrder(BaseModel):
    __tablename__="lab_orders"
    patient_id: Mapped[UUID]=mapped_column(ForeignKey("patients.id"),index=True)
    lab_test_id: Mapped[UUID]=mapped_column(ForeignKey("lab_tests.id"))
    appointment_id: Mapped[UUID|None]=mapped_column(ForeignKey("appointments.id"),nullable=True)
    status: Mapped[LabOrderStatus]=mapped_column(Enum(LabOrderStatus),default=LabOrderStatus.ORDERED)
    result: Mapped[str|None]=mapped_column(Text,nullable=True)
    notes: Mapped[str|None]=mapped_column(Text,nullable=True)
    completed_at: Mapped[datetime|None]=mapped_column(nullable=True)
