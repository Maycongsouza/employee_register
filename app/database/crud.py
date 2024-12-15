from sqlalchemy.orm import Session
from app.models.department import Department as DepartmentModel
from app.models.job import Job as JobModel
from app.models.user import User as UserModel
from app.models.employee import Employee as EmployeeModel, StateEnum
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.schemas.job import JobCreate, JobUpdate
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from typing import List

def create_employee(db: Session, employee: EmployeeCreate) -> EmployeeModel:
    db_employee = EmployeeModel(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_all_employees(db: Session) -> List[EmployeeModel]:
    return db.query(EmployeeModel).all()

def get_employee_by_id(db: Session, employee_id: int) -> EmployeeModel:
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()
    if not employee:
        return None
    return employee

def promote_employee(db: Session, employee_id: int, update_data: EmployeeUpdate) -> EmployeeModel:
    employee = get_employee_by_id(db, employee_id)

    if update_data.name:
        employee.name = update_data.name
    if update_data.last_name:
        employee.last_name = update_data.last_name
    if update_data.job_id:
        employee.job_id = update_data.job_id
    if update_data.salary:
        employee.salary = update_data.salary

    db.commit()
    db.refresh(employee)
    return employee

def terminate_employee(db: Session, employee_id: int) -> EmployeeModel:
    employee = get_employee_by_id(db, employee_id)

    employee.status = StateEnum.archived
    db.commit()
    db.refresh(employee)
    return employee

def delete_employee(db: Session, employee_id: int) -> None:
    employee = get_employee_by_id(db, employee_id)

    db.delete(employee)
    db.commit()

# CRUD for Department
def create_department(db: Session, department: DepartmentCreate) -> DepartmentModel:
    db_department = DepartmentModel(**department.dict())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def get_all_departments(db: Session) -> List[DepartmentModel]:
    return db.query(DepartmentModel).all()

def get_department_by_id(db: Session, department_id: int) -> DepartmentModel:
    department = db.query(DepartmentModel).filter(DepartmentModel.id == department_id).first()
    if not department:
        return None
    return department

def update_department(db: Session, department_id: int, update_data: DepartmentUpdate) -> DepartmentModel:
    department = get_department_by_id(db, department_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(department, field, value)
    db.commit()
    db.refresh(department)
    return department

def delete_department(db: Session, department_id: int) -> None:
    department = get_department_by_id(db, department_id)
    db.delete(department)
    db.commit()

# CRUD for Job
def create_job(db: Session, job: JobCreate) -> JobModel:
    db_job = JobModel(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_all_jobs(db: Session) -> List[JobModel]:
    return db.query(JobModel).all()

def get_job_by_id(db: Session, job_id: int) -> JobModel:
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    if not job:
        return None
    return job

def update_job(db: Session, job_id: int, update_data: JobUpdate) -> JobModel:
    job = get_job_by_id(db, job_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job

def delete_job(db: Session, job_id: int) -> None:
    job = get_job_by_id(db, job_id)
    db.delete(job)
    db.commit()

# CRUD for User
def create_user(db: Session, user: UserCreate) -> UserModel:
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).all()

def get_user_by_id(db: Session, user_id: int) -> UserModel:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return None
    return user

def update_user(db: Session, user_id: int, update_data: UserUpdate) -> UserModel:
    user = get_user_by_id(db, user_id)
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user_id: int, update_data: UserUpdate) -> UserModel:
    user = get_user_by_id(db, user_id)
    user.passw = update_data.passw  # Assumindo que a senha será hash antes
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
