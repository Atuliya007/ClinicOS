from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.modules.departments.models import Department
from app.modules.departments.schemas import DepartmentCreate, DepartmentResponse, DepartmentUpdate
router = APIRouter(prefix="/departments", tags=["Departments"])
@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create(data: DepartmentCreate, db: Session = Depends(get_db)):
    if db.scalar(select(Department).where(Department.name == data.name)): raise HTTPException(409, "Department name already exists")
    latest = db.scalar(select(Department).order_by(Department.department_code.desc()).limit(1))
    item = Department(department_code=f"DP{(int(latest.department_code[2:]) + 1) if latest else 1:06d}", **data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@router.get("", response_model=list[DepartmentResponse])
def list_items(db: Session = Depends(get_db)): return list(db.scalars(select(Department)).all())
@router.patch("/{item_id}", response_model=DepartmentResponse)
def update(item_id: UUID, data: DepartmentUpdate, db: Session = Depends(get_db)):
    item = db.get(Department, item_id)
    if not item: raise HTTPException(404, "Department not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(item,k,v)
    db.commit(); db.refresh(item); return item
