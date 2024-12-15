try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.department import Department as DepartmentSchema, DepartmentCreate, DepartmentUpdate
    from app.database import crud
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)

router = APIRouter()


# Department Routes
@router.post("/", response_model=DepartmentSchema)
def create_department_route(department: DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)

@router.get("/", response_model=List[DepartmentSchema])
def get_all_departments_route(db: Session = Depends(get_db)):
    return crud.get_all_departments(db)

@router.get("/{department_id}", response_model=DepartmentSchema)
def get_department_route(department_id: int, db: Session = Depends(get_db)):
    return crud.get_department_by_id(db, department_id)

@router.put("/{department_id}", response_model=DepartmentSchema
)
def update_department_route(department_id: int, update_data: DepartmentUpdate, db: Session = Depends(get_db)):
    return crud.update_department(db, department_id, update_data)

@router.delete("/{department_id}")
def delete_department_route(department_id: int, db: Session = Depends(get_db)):
    crud.delete_department(db, department_id)
    return {"message": "Departamento deletado com sucesso"}