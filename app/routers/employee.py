try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.employee import Employee as EmployeeSchema, EmployeeCreate, EmployeeUpdate
    from app.database import crud
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)

router = APIRouter()


@router.post("/", response_model=EmployeeSchema)
def create_employee_route(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

@router.get("/", response_model=List[EmployeeSchema])
def get_all_employees_route(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)

@router.get("/{employee_id}", response_model=EmployeeSchema)
def get_employee_route(employee_id: int, db: Session = Depends(get_db)):
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador com ID %s não encontrado" % employee_id)
    return employee

@router.put("/{employee_id}/promote", response_model=EmployeeSchema)
def promote_employee_route(employee_id: int, update_data: EmployeeUpdate, db: Session = Depends(get_db)):
    return crud.promote_employee(db, employee_id, update_data)

@router.put("/{employee_id}/archive", response_model=EmployeeSchema)
def terminate_employee_route(employee_id: int, db: Session = Depends(get_db)):
    return crud.terminate_employee(db, employee_id)

@router.delete("/{employee_id}")
def delete_employee_route(employee_id: int, db: Session = Depends(get_db)):
    crud.delete_employee(db, employee_id)
    return {"message": "Colaborador deletado com sucesso"}