from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel,Field
from app.enums.laboratory import LabOrderStatus
class LabTestCreate(BaseModel): name:str; price:Decimal=Field(ge=0); description:str|None=None
class LabTestResponse(LabTestCreate): id:UUID;test_code:str;is_active:bool;model_config={"from_attributes":True}
class LabOrderCreate(BaseModel): patient_id:UUID;lab_test_id:UUID;appointment_id:UUID|None=None;notes:str|None=None
class LabOrderUpdate(BaseModel): status:LabOrderStatus|None=None;result:str|None=None;notes:str|None=None
class LabOrderResponse(LabOrderCreate): id:UUID;status:LabOrderStatus;result:str|None=None;model_config={"from_attributes":True}
