from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel,Field
class MedicineCreate(BaseModel):name:str;description:str|None=None;unit_price:Decimal=Field(ge=0);stock_quantity:int=Field(ge=0);reorder_level:int=Field(ge=0)
class MedicineResponse(MedicineCreate):id:UUID;medicine_code:str;is_active:bool;model_config={"from_attributes":True}
class PrescriptionItemCreate(BaseModel):medicine_id:UUID;quantity:int=Field(gt=0);dosage:str
class PrescriptionCreate(BaseModel):patient_id:UUID;doctor_id:UUID;appointment_id:UUID|None=None;notes:str|None=None;items:list[PrescriptionItemCreate]=Field(min_length=1)
class PrescriptionResponse(BaseModel):id:UUID;patient_id:UUID;doctor_id:UUID;notes:str|None=None;model_config={"from_attributes":True}
