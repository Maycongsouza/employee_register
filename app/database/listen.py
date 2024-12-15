from sqlalchemy.event import listens_for
from app.models.employee import Employee
from app.models.job import Job
from app.models.department import Department
from app.models.user import User

@listens_for(Employee, "before_insert")
def validate_job_before_insert(mapper, connection, target: Employee):
    job = connection.execute(
        Job.__table__.select().where(Job.id == target.job_id)
    ).fetchone()
    if not job:
        raise ValueError("Cargo inválido.")
    target.department_id = job.department_id

@listens_for(Employee, "before_update")
def validate_job_before_insert(mapper, connection, target: Employee):
    job = connection.execute(
        Job.__table__.select().where(Job.id == target.job_id)
    ).fetchone()
    if not job:
        raise ValueError("Cargo inválido.")
    target.department_id = job.department_id