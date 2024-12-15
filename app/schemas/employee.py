from pydantic import BaseModel
from typing import Optional


class EmployeeBase(BaseModel):
    name: str
    last_name: str
    register_number: str
    job_id: int
    department_id: Optional[int] = None
    salary: float
    status: Optional[str] = "active"


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    job_id: Optional[int] = None
    salary: Optional[float] = None
    status: Optional[str] = None


class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True
