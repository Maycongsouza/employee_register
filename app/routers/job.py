try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.job import Job as JobSchema, JobCreate, JobUpdate
    from app.database import crud
except Exception as error:
    raise ImportError("Erro de biblioteca: %s" % error)

router = APIRouter()


# Job Routes
@router.post("/", response_model=JobSchema)
def create_job_route(job: JobCreate, db: Session = Depends(get_db)):
    """
        Rota para criar um novo cargo.

        Args:
            job: Dados do cargo que deve ser criado.
            db: Sessão do banco de dados.

        Returns:
            JobResponse: Retorna os detalhes do cargo criado.
    """

    return crud.create_job(db, job)

@router.get("/", response_model=List[JobSchema])
def get_all_jobs_route(db: Session = Depends(get_db)):
    """
        Rota para listar todos os cargos.

        Args:
        db: Sessão do banco de dados.

        Returns:
        List[JobResponse]: Retorna a lista de todos os cargos.
    """

    return crud.get_all_jobs(db)

@router.get("/{job_id}", response_model=JobSchema)
def get_job_route(job_id: int, db: Session = Depends(get_db)):
    """
        Rota para buscar as informações de um cargo específico pelo ID.

        Args:
        job_id: ID do cargo.
        db: Sessão do banco de dados.

        Returns:
        JobResponse: Retorna os detalhes do cargo correspondente.
    """

    return crud.get_job_by_id(db, job_id)

@router.put("/{job_id}", response_model=JobSchema)
def update_job_route(job_id: int, update_data: JobUpdate, db: Session = Depends(get_db)):
    """
        Rota para atualizar as informações de um cargo.

        Args:
        job_id: ID do cargo a ser atualizado.
        update_data: Dados que devem atualizar o registro do cargo no banco.
        db: Sessão do banco de dados.

        Returns:
        JobResponse: Retornar os detalhes do cargo atualizado.
    """

    return crud.update_job(db, job_id, update_data)

@router.delete("/{job_id}")
def delete_job_route(job_id: int, db: Session = Depends(get_db)):
    """
        Rota para excluir um cargo.

        Args:
        job_id: ID do cargo selecionado para ser deletado.
        db: Sessão do banco de dados.

        Returns:
        message: Retorna mensagem avisando que foi deletado.
    """

    crud.delete_job(db, job_id)
    return {"message": "Cargo deletado com sucesso"}