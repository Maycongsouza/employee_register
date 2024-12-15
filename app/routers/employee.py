try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.employee import Employee as EmployeeSchema, EmployeeCreate, EmployeeUpdate
    from app.database import crud
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

router = APIRouter()


@router.post("/", response_model=EmployeeSchema)
def create_employee_route(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """
        Rota que registra um novo colaborador no banco.

        Args:
            employee: Dados do colaborador a serem inseridos.
            db: Sessão do banco de dados.

        Returns:
            EmployeeResponse: Detalhamento do colaborador recém-criado.
    """

    return crud.create_employee(db, employee)

@router.get("/", response_model=List[EmployeeSchema])
def get_all_employees_route(db: Session = Depends(get_db)):
    """
        Rota que faz uma listagem de todos os colaboradores.

        Args:
            db: Sessão do banco de dados.

        Returns:
            List[EmployeeResponse]: Lista de todos os colaboradores.
    """

    return crud.get_all_employees(db)

@router.get("/{employee_id}", response_model=EmployeeSchema)
def get_employee_route(employee_id: int, db: Session = Depends(get_db)):
    """
        Rota que busca as informações de um colaborador pelo ID.

        Args:
            db: Sessão do banco de dados.
            employee_id: ID do colaborador a ser selecionado.

        Returns:
            EmployeeResponse: Colaborador buscado pelo ID
    """

    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Colaborador com ID %s não encontrado" % employee_id)
    return employee

@router.put("/{employee_id}/promote", response_model=EmployeeSchema)
def promote_employee_route(employee_id: int, update_data: EmployeeUpdate, db: Session = Depends(get_db)):
    """
        Rota para atualizar ou 'promover' um colaborador.

        Args:
        employee_id: ID do colaborador a ser atualizado.
        update_data: Dados que deverão ser atualizados.
        db: Sessão do banco de dados.

        Returns:
        EmployeeResponse: Retorna os detalhes do colaborador atualizado.
    """

    return crud.promote_employee(db, employee_id, update_data)

@router.put("/{employee_id}/archive", response_model=EmployeeSchema)
def terminate_employee_route(employee_id: int, db: Session = Depends(get_db)):
    """
        Rota para atualizar o status do colaborador para ARQUIVADO.

        Args:
        employee_id: ID do colaborador a ser arquivado.
        db: Sessão do banco de dados.

        Returns:
        EmployeeResponse: Retorna os detalhes do colaborador arquivado.
    """

    return crud.terminate_employee(db, employee_id)

@router.delete("/{employee_id}")
def delete_employee_route(employee_id: int, db: Session = Depends(get_db)):
    """
        Rota para excluir um colaborador.

        Args:
        employee_id: ID do colaborador a ser excluído do banco.
        db: Sessão do banco de dados.

        Returns:
        message: Apenas retorna mensagem informativa
    """

    crud.delete_employee(db, employee_id)
    return {"message": "Colaborador deletado com sucesso"}