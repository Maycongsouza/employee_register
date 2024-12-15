try:
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from typing import List
    from app.database.conn import get_db
    from app.schemas.job import Job as JobSchema, JobCreate, JobUpdate
    from app.database import crud
except Exception as error:
    raise ("Erro de biblioteca: %s" % error)

router = APIRouter()


# Job Routes
@router.post("/", response_model=JobSchema)
def create_job_route(job: JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)

@router.get("/", response_model=List[JobSchema])
def get_all_jobs_route(db: Session = Depends(get_db)):
    return crud.get_all_jobs(db)

@router.get("/{job_id}", response_model=JobSchema)
def get_job_route(job_id: int, db: Session = Depends(get_db)):
    return crud.get_job_by_id(db, job_id)

@router.put("/{job_id}", response_model=JobSchema)
def update_job_route(job_id: int, update_data: JobUpdate, db: Session = Depends(get_db)):
    return crud.update_job(db, job_id, update_data)

@router.delete("/{job_id}")
def delete_job_route(job_id: int, db: Session = Depends(get_db)):
    crud.delete_job(db, job_id)
    return {"message": "Cargo deletado com sucesso"}