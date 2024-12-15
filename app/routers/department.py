try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.department import Department as DepartmentSchema, DepartmentCreate, DepartmentUpdate
    from app.database import crud
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

router = APIRouter()


# Department Routes
@router.post("/", response_model=DepartmentSchema)
def create_department_route(department: DepartmentCreate, db: Session = Depends(get_db)):
    """
        Rota para criar um novo departamento.

        Args:
            department: Dados do departamento a serem inseridos no banco.
            db: Sessão do banco de dados.

        Returns:
            DepartmentResponse: Lista os detalhes do departamento criado.
    """

    return crud.create_department(db, department)

@router.get("/", response_model=List[DepartmentSchema])
def get_all_departments_route(db: Session = Depends(get_db)):
    """
    Rota para listar todos os departamentos.

    Args:
        db: Sessão do banco de dados.

    Returns:
        List[DepartmentResponse]: Retorna a lista de todos os departamentos inseridos no banco.
    """

    return crud.get_all_departments(db)

@router.get("/{department_id}", response_model=DepartmentSchema)
def get_department_route(department_id: int, db: Session = Depends(get_db)):
    """
        Rota para buscar um departamento específico pelo ID.

        Args:
            department_id: ID do departamento.
            db: Sessão do banco de dados.

        Returns:
            DepartmentResponse: Listar detalhes do departamento correspondente.
    """

    return crud.get_department_by_id(db, department_id)

@router.put("/{department_id}", response_model=DepartmentSchema
)
def update_department_route(department_id: int, update_data: DepartmentUpdate, db: Session = Depends(get_db)):
    """
        Rota para atualizar um departamento específico pelo ID.

        Args:
            department_id: ID do departamento.
            update_data: Dados correspondentes para atualizar o departamento.
            db: Sessão do banco de dados.

        Returns:
            DepartmentResponse: Listar detalhes do departamento com os dados atualizados.
    """

    return crud.update_department(db, department_id, update_data)

@router.delete("/{department_id}")
def delete_department_route(department_id: int, db: Session = Depends(get_db)):
    """
        Rota para deletar um departamento específico pelo ID.

        Args:
            department_id: ID do departamento.
            db: Sessão do banco de dados.

        Returns:
            message: Informativo que o departamento foi deletado.
    """

    crud.delete_department(db, department_id)
    return {"message": "Departamento deletado com sucesso"}