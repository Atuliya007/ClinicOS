from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.enums.receptionist import Shift
from app.modules.receptionists.schemas import ReceptionistCreate, ReceptionistResponse, ReceptionistUpdate
from app.modules.receptionists.service import ReceptionistService

router = APIRouter(prefix="/receptionists", tags=["Receptionists"])
service = ReceptionistService()

@router.post("", response_model=ReceptionistResponse, status_code=status.HTTP_201_CREATED)
def create(data: ReceptionistCreate, db: Session = Depends(get_db)): return service.create(db, data)
@router.get("", response_model=list[ReceptionistResponse])
def list_items(active: bool | None = Query(None), shift: Shift | None = Query(None), db: Session = Depends(get_db)): return service.repository.filtered(db, active, shift)
@router.get("/{item_id}", response_model=ReceptionistResponse)
def get(item_id: UUID, db: Session = Depends(get_db)): return service.get(db, item_id)
@router.patch("/{item_id}", response_model=ReceptionistResponse)
def update(item_id: UUID, data: ReceptionistUpdate, db: Session = Depends(get_db)): return service.update(db, item_id, data)
